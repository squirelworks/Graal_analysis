"""In-process checks for the 2.22 generator references. No sockets, no files from Drive."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dungeon
import levelgen
import nwtext
import terrain


class NoSocket(unittest.TestCase):
    def test_modules_do_not_import_socket(self):
        for module in (nwtext, terrain, dungeon, levelgen):
            self.assertNotIn('socket', module.__dict__)


class BoardRoundTrip(unittest.TestCase):
    def test_tile_zero_is_a_row_of_a(self):
        tiles = [0] * (64 * 64)
        tiles[64 + 3] = 1
        text = nwtext.level_text(tiles)
        self.assertTrue(text.startswith('GLEVNW01\n'))
        self.assertIn('BOARD 0 0 64 0 ' + ('A' * 128), text)
        self.assertEqual(nwtext.parse_board(text)[64 + 3], 1)
        self.assertEqual(nwtext.parse_board(text)[0], 0)


class Terrain(unittest.TestCase):
    def test_seed_repeats_and_even_border_stays_at_base(self):
        first = terrain.generate('isle', 7, width=2, height=2, base=10,
                                  amplitude=40, chaos=0.5, even_borders=True)
        second = terrain.generate('isle', 7, width=2, height=2, base=10,
                                   amplitude=40, chaos=0.5, even_borders=True)
        self.assertEqual(first, second)
        other = terrain.generate('isle', 8, width=2, height=2, base=10,
                                  amplitude=40, chaos=0.5, even_borders=True)
        self.assertNotEqual(first['isle.gmap'], other['isle.gmap'])
        gmap = first['isle.gmap']
        self.assertIn('GENERATED 1\n', gmap)
        self.assertIn('GENEVENBORDERS 1\n', gmap)
        self.assertIn('MAPIMG isle.png\n', gmap)
        self.assertIn('isleA00.nw\nisleB00.nw\nisleA01.nw\nisleB01.nw\n', gmap)
        level = first['isleA00.nw']
        self.assertIn('HEIGHTS\n', level)
        self.assertIn('HEIGHTSEND\n', level)
        self.assertIn('LINK isleB00.nw 63 0 1 64 0 playery', level)
        self.assertIn('LINK isleA01.nw 0 63 64 1 playerx 0', level)
        self.assertNotIn('LINK isle', level.split('HEIGHTS')[0])
        rows = [line for line in level.splitlines() if line[:1].isdigit() or line.startswith('-')]
        self.assertEqual(len(rows), 9)
        self.assertEqual(len(rows[0].split()), 9)
        self.assertTrue(rows[0].startswith('10 '))
        self.assertTrue(all(line.startswith('BOARD 0 ') for line in level.splitlines() if line.startswith('BOARD')))

    def test_islands_force_even_borders_and_a_single_level_has_no_link(self):
        files = terrain.generate('one', 3, width=1, height=1, islands=True, base=4)
        self.assertIn('GENEVENBORDERS 1\n', files['one.gmap'])
        self.assertNotIn('LINK ', files['oneA00.nw'])
        self.assertEqual(files['one.gmap'].count('RANDOMSEEDS\n') , 1)


class Dungeon(unittest.TestCase):
    def test_hand_drawn_room_facings_and_gmap(self):
        layout = '\n'.join([
            'XXXXXXXX',
            'X......X',
            'X......X',
            'X......X',
            'XXXXXXXX',
        ])
        options = '\n'.join([
            'GDUNG001',
            'LEVELSTART cave_',
            'GMAP cave',
            'LAYOUTFILE room.txt',
            'ADDTESTNPCS',
            'NPC image=torch.png,blocking=false,chance=100%,place=walln,x=3,y=5',
            'NPC image=lamp.png,blocking=false,underplayer=true,chance=0%,place=path,x=1,y=1',
        ])
        files = dungeon.generate(options, layouts={'room.txt': layout})
        self.assertIn('cave.gmap', files)
        self.assertEqual(
            files['cave.gmap'],
            'GRMAP001\nWIDTH 1\nHEIGHT 1\nGENERATED cave_A1.nw\n',
        )
        level = files['cave_A1.nw']
        self.assertIn('if (playerenters)', level)
        self.assertIn('loadmap cave;', level)
        self.assertIn('NPC torch.png 27 5', level)
        self.assertIn('dontblock;', level)
        self.assertNotIn('lamp.png', level)
        places = dungeon.classify(dungeon.load_layout(layout))
        self.assertEqual(places[0][3], 'walln')
        self.assertEqual(places[2][0], 'wallw')
        self.assertEqual(places[2][7], 'walle')
        self.assertEqual(places[4][3], 'walls')
        self.assertEqual(places[0][0], 'wallnw')
        self.assertEqual(places[2][2], 'path')
        tiles = nwtext.parse_board(level)
        self.assertEqual(tiles[0], 1)
        self.assertEqual(tiles[3], 1)
        self.assertEqual(tiles[10 * 64 + 3], 0)

    def test_tiles_override_and_symmetry_and_maze_seed(self):
        ids = ','.join(['7'] * (8 * 11))
        options = '\n'.join([
            'GDUNG001',
            'LEVELSTART t_',
            'GMAP t',
            'LAYOUTWIDTH 8',
            'LAYOUTHEIGHT 8',
            'LAYOUTSTYLE maze',
            'DOUBLE 0',
            'LAYOUTSYMMETRY 2',
            'RANDOMSEED 99',
            'TILES wall=%s' % ids,
            'TILES path=%s' % ','.join(['3'] * 88),
        ])
        files = dungeon.generate(options)
        again = dungeon.generate(options)
        self.assertEqual(files, again)
        grid = dungeon.styled_layout('maze', 8, 8, 0, 0, 2, 99)
        for y in range(8):
            for x in range(4):
                self.assertEqual(grid[y][x], grid[y][7 - x])
        level = files['t_A1.nw']
        tiles = nwtext.parse_board(level)
        self.assertIn(7, tiles)
        self.assertIn(3, tiles)

    def test_styles_cover_the_manual_names(self):
        for style in ('maze', 'onion', 'spiral', 'rogue', 'snake', 'squarespiral'):
            grid = dungeon.styled_layout(style, 12, 12, 1, 1, 1, 5)
            self.assertEqual(len(grid), 12)
            self.assertEqual(len(grid[0]), 12)
            flat = ''.join(''.join(row) for row in grid)
            self.assertIn('.', flat)
            self.assertIn('X', flat)

    def test_chance_without_percent_sign(self):
        rule = dungeon._npc_rule('chance=100,place=path,x=0,y=0')
        self.assertEqual(rule['chance'], 1.0)
        rule = dungeon._npc_rule('chance=30%,place=walln,x=0,y=0')
        self.assertAlmostEqual(rule['chance'], 0.30)


class LevelGen(unittest.TestCase):
    def _image(self, width, height, colour):
        return [colour] * (width * height)

    def test_grass_is_empty_and_forest_stamp_lands(self):
        pixels = self._image(64, 64, (24, 140, 24))
        pixels[0] = (181, 239, 189)
        files = levelgen.generate('world', pixels, 64, 64)
        tiles = nwtext.parse_board(files['world_a-01.nw'])
        self.assertEqual(tiles[0], 0)
        self.assertEqual(tiles[1 * 64 + 0], 25)
        self.assertEqual(tiles[1 * 64 + 5], 30)
        self.assertEqual(tiles[5 * 64 + 0], 89)
        gmap = files['world.gmap']
        self.assertIn('LEVELNAMES\n"world_a-01.nw",\nLEVELNAMESEND\n', gmap)
        self.assertNotIn('LINK ', files['world_a-01.nw'])

    def test_distance_limit_and_two_levels(self):
        self.assertEqual(levelgen.match_colour((24, 140, 24)), 0)
        self.assertEqual(levelgen.match_colour((24, 140, 50)), 0)
        self.assertIsNone(levelgen.match_colour((24, 140, 56)))
        self.assertEqual(levelgen.match_colour((0, 0, 255)), 2)
        pixels = self._image(128, 64, (0, 0, 0))
        pixels[0] = (0, 0, 255)
        # Cell sample points sit on multiples of 6. x=66 is the first sample in level b.
        pixels[66] = (128, 0, 0)
        files = levelgen.generate('sea', pixels, 128, 64)
        self.assertIn('LINK sea_b-01.nw 63 0 1 64 0 playery', files['sea_a-01.nw'])
        self.assertIn('LINK sea_a-01.nw 0 0 1 64 61 playery', files['sea_b-01.nw'])
        left = nwtext.parse_board(files['sea_a-01.nw'])
        right = nwtext.parse_board(files['sea_b-01.nw'])
        self.assertEqual(left[0], 12)
        self.assertEqual(right[2], 80)
        self.assertIn('"sea_a-01.nw","sea_b-01.nw",', files['sea.gmap'])

    def test_second_run_keeps_old_tiles_and_npcs(self):
        pixels = self._image(64, 64, (24, 140, 24))
        pixels[6] = (255, 0, 0)
        old_tiles = [0] * (64 * 64)
        old_tiles[2] = 9
        old = nwtext.level_text(
            old_tiles,
            links=['LINK kept.nw 1 2 3 4 5 6'],
            npcs=[nwtext.npc_block('npc.png', 4, 5, 'if (created) say 1;')],
        )
        files = levelgen.generate(
            'world', pixels, 64, 64,
            existing={'world_a-01.nw': old},
        )
        tiles = nwtext.parse_board(files['world_a-01.nw'])
        self.assertEqual(tiles[2], 9)
        self.assertEqual(tiles[6], 4)
        self.assertIn('LINK kept.nw 1 2 3 4 5 6', files['world_a-01.nw'])
        self.assertIn('NPC npc.png 4 5', files['world_a-01.nw'])
        self.assertIn('say 1;', files['world_a-01.nw'])


if __name__ == '__main__':
    unittest.main()
