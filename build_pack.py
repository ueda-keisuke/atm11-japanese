#!/usr/bin/env python3
"""Build a collection of independently licensed Japanese language assets from pinned evidence."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION = '0.6.0'
TRANSMOG_FILTER = {'block': [{'namespace': '^transmog$', 'path': r'^lang/ja_jp\.json$'}]}
POLICIES = {'transmog': {'version': '1.8.0+26.1',
              'jar_sha256': '71236a1adcec1a6186828c49dd22d330054db30f7372b8d8be25a1c58d704ba7',
              'jar_entry': 'assets/transmog/lang/en_us.json',
              'source_sha256': '89ebb4d6af7d4da87fafaa8e69534b29534a68e6af8532f6d5bc2ea88412be5f'},
 'jei': {'version': '29.36.0.96',
         'jar_sha256': 'a4ac2d91b2f86e56275316ac185208d275edcca6d975998a93cc6e604910c07d',
         'jar_entry': 'assets/jei/lang/en_us.json',
         'source_sha256': 'b39dc5633aeadb953a671ac50e58a26951b20593473995bbf93a389caae108e1'},
 'appleskin': {'version': '3.0.9',
               'jar_sha256': '32bfe1ed3dea0684259568dbf2b6fe02e939bf398e54af383238bb3b8cac4da6',
               'jar_entry': 'assets/appleskin/lang/en_us.json',
               'source_sha256': 'e4ecdf6e503c5e9a63277b1092c7221671724959907152ac18cef12cc59f7075'},
 'controlling': {'version': '26.1.2.4',
                 'jar_sha256': '16289226a72a8709d77e2f477beaf276d4a90583efc712c6114811fd1a3a3f51',
                 'jar_entry': 'assets/controlling/lang/en_us.json',
                 'source_sha256': 'ddd09483c4b6c3b898ca28e3b22e8fb4b042abc402bdef50c1a12cb49fe27725'},
 'jade': {'version': '26.1.10',
          'jar_sha256': 'd1e477ed030f96605a2471c0d2003846a90cc12c4059782e62cdee2d4c529fc7',
          'jar_entry': 'assets/jade/lang/en_us.json',
          'source_sha256': '799373d21b23e9a8fda3158ff4d098e4d1e6cf99eb2b935836650dce4a459153'},
 'searchables': {'version': '1.0.2',
                 'jar_sha256': '85466d9b55239f5a13afcd41ec7eef816074427c5cd1080e740205ab8d7825b3',
                 'jar_entry': 'assets/searchables/lang/en_us.json',
                 'source_sha256': '48de13a3fd577126aab0b5f46d18d4320472000fc7688af4da03b8918c9db42c'},
 'resourcefulconfig': {'version': '4.0.1',
                       'source_type': 'nested_jar_lang',
                       'source': 'minecraft/mods/lootr-neoforge-26.1.2-1.23.38.120.jar',
                       'jar_sha256': '2a1c188deaf52f3c0e8baab0ba2c0bdd76c326a1184f8945d6f56f45a7a24521',
                       'archive_chain': [{'entry': 'META-INF/jarjar/resourcefulconfig-neoforge-26.1-4.0.1.jar',
                                          'sha256': 'c2725f7f2f077f2746acfc5fad997d8510319425c45ee4c1a2ea8d968db324f1'}],
                       'jar_entry': 'assets/resourcefulconfig/lang/en_us.json',
                       'source_sha256': '477bdad1482cddac869c98c2e1570ff2e348334e974feb24e1b8f5c298b848cd',
                       'namespace': 'resourcefulconfig',
                       'locale': 'ja_jp',
                       'catalog_source_id': 'de7d57b27cd61b07933432ff973d0c45d4d2a55cd356c61e2e645fc0ff74259e'},
 'ae2netanalyser': {'version': '26.1-1.0.0-neoforge',
                    'jar_sha256': 'ef3c4c7c326e429d725108226299da0fe91bbff0bf9fe8fe2bfc287a2c66fca3',
                    'jar_entry': 'assets/ae2netanalyser/lang/en_us.json',
                    'source_sha256': '0d3de4617d24f082e8e633e02e7884fea695449b3783d662cdc2dceb92bc4e5c'},
 'cumulus_menus': {'version': '2.0.15',
                   'source_type': 'nested_jar_lang',
                   'source': 'minecraft/mods/aether_ii-26.1.2-alpha.4.1-neoforge.jar',
                   'jar_sha256': '97760dd75e2dcdf4ecde83a0006d5b3682090e104a3c7bd6d7e4681e33b3f0e6',
                   'archive_chain': [{'entry': 'META-INF/jarjar/cumulus_menus-26.1.2-2.0.15-neoforge.jar',
                                      'sha256': '9cff5f97963c247aa810f5b23a712dc7e6d288b5c06732d07776d79417eb3dbd'}],
                   'jar_entry': 'assets/cumulus_menus/lang/en_us.json',
                   'source_sha256': '181edddff82f182f5208b0d3693872164153464429bcc6b48a5e17eb0693dca2',
                   'namespace': 'cumulus_menus',
                   'locale': 'ja_jp',
                   'catalog_source_id': 'ec02354331ac976f2206aa0816d2f535a9ce305c36415820cc7f749616453a1c'},
 'sodium': {'version': '0.9.1',
            'source_type': 'nested_jar_lang',
            'source': 'minecraft/mods/sodium-neoforge-0.9.1+mc26.1.2.jar',
            'jar_sha256': 'ec907b646997d1f04ccc53ed6b48b9b343c096fdf17212b640e5fb54e3c1b200',
            'archive_chain': [{'entry': 'META-INF/jarjar/net.caffeinemc.sodium-neoforge-0.9.1+mc26.1.2-mod.jar',
                               'sha256': '73780c4ee946bf7c4be7ee8ba8feaf0cd573b8df46b88d7b65e15ab9135ddde1'}],
            'jar_entry': 'assets/sodium/lang/en_us.json',
            'source_sha256': '86bd13ad78a86878c1cf6bd900ad076db2d471fab6058352e6ef66eb0b75618e',
            'namespace': 'sodium',
            'locale': 'ja_jp',
            'catalog_source_id': 'e88743903cdc5005590f0e301b0c773004dee26e33573875abbaa46a44a6bd9a'},
 'betteradvancements': {'version': '0.6.0.76',
                        'jar_sha256': '6399badfcb0677afd01dfa345b743d41b43cdb146b7c9732a72d20be2f7dad05',
                        'jar_entry': 'assets/betteradvancements/lang/en_us.json',
                        'source_sha256': 'cc556d46058c7c2555984349a976ae2e87b322bcd0877eb4d883be500d7bce3f'},
 'codedefinedgui': {'version': '1.12.0',
                    'jar_sha256': '874c46d9cc5075b01d7e1b06485b7e2ad1e53adea6bdc270efeeaec3934bedfa',
                    'jar_entry': 'assets/codedefinedgui/lang/en_us.json',
                    'source_sha256': '6ab41a3ebcc3d112956015914b8b98adbe88989d3e1acb1708552ca3e4bffd77',
                    'source_type': 'nested_jar_lang',
                    'source': 'minecraft/mods/theurgy-26.1.2-neoforge-1.114.0.jar',
                    'archive_chain': [{'entry': 'META-INF/jarjar/codedefinedgui-26.1.2-neoforge-1.12.0.jar',
                                       'sha256': 'ef9704b03bf028fb060cbcd8daf470ec7a87ff3d433baf9703a73ed13a1834e4'}],
                    'namespace': 'codedefinedgui',
                    'locale': 'ja_jp',
                    'catalog_source_id': '059d2be0ba6024526cb6a9650d09640895c7b05b39dd262922173d2854aba776'},
 'sathlib': {'version': '1.1.0+26.1.2',
             'jar_sha256': '4a6be925d75625e4a09abbc62ccfe1b1b69e768e499b68fd55f5bc3b93026a2a',
             'jar_entry': 'assets/sathlib/lang/en_us.json',
             'source_sha256': '0e71b621896f1632fb3b182a155d167ba4473c8b5da4cb1fea36f159b57b44ab',
             'source_type': 'nested_jar_lang',
             'source': 'minecraft/mods/crystalix-4.1.0+26.1.2.jar',
             'archive_chain': [{'entry': 'META-INF/jarjar/sathlib-1.1.0+26.1.2.jar',
                                'sha256': '78afee725f643072f4fc04241afec64c2d0c1d66f4600df8d406c878f8c280e1'}],
             'namespace': 'sathlib',
             'locale': 'ja_jp',
             'catalog_source_id': '66f84f1cf694905f7d9d22748f1743b0f96d3850cb303ad3fc2f326740fcb65e'},
 'ae2addonlib': {'version': '26.1.3-alpha',
                 'jar_sha256': 'fae810b62ecd1746ab9b74ba6e0b5242ab7c0e92d291704e4ea755c83230b233',
                 'jar_entry': 'assets/ae2addonlib/lang/en_us.json',
                 'source_sha256': '2ea255e03c6e800750f90011148a2559b04090212fb881c1db0bfe718ee433c7',
                 'source_type': 'nested_jar_lang',
                 'source': 'minecraft/mods/AdvancedAE-26.1.7.jar',
                 'archive_chain': [{'entry': 'META-INF/jarjar/ae2addonlib-26.1.3-alpha.jar',
                                    'sha256': '15a8598e48acd2613b63d822cf416b36b1793cbca7c2a383828a1e0cbfd5ee5b'}],
                 'namespace': 'ae2addonlib',
                 'locale': 'ja_jp',
                 'catalog_source_id': 'd8569804156631d1c882b17eff6ec06243100774c1517eafb8cb39c81694d85d'},
 'ae2wtlib_api': {'version': '26.1.1-beta',
                  'jar_sha256': '9309564ee5f3640ddbcc55450e0727e5a7790488f3b82af350d3012960b18311',
                  'jar_entry': 'assets/ae2wtlib_api/lang/en_us.json',
                  'source_sha256': '0fda89f6cc1a08aa46279dd5e178fcced86df902cf11828f98c513e17b41e9c4',
                  'source_type': 'nested_jar_lang',
                  'source': 'minecraft/mods/ae2wtlib-26.1.1-beta.jar',
                  'archive_chain': [{'entry': 'META-INF/jarjar/de.mari_023.ae2wtlib_api-26.1.1-beta.jar',
                                     'sha256': '95f039edafe427a8f363afdc19df5b49e04c73bd90463e45b5c84251e104b148'}],
                  'namespace': 'ae2wtlib_api',
                  'locale': 'ja_jp',
                  'catalog_source_id': '9d4f7d0087b58c18f6bbf95f9b8a55fb7e99c23b8c79c82d9c717810d9d2f5e4'},
 'kuma_api': {'version': '26.1.2.2',
              'jar_sha256': 'aeb1d1962e9d2e1bc6345bd91bef9a6b3ab88cdff1495c8a360a6e711313fa37',
              'jar_entry': 'assets/kuma_api/lang/en_us.json',
              'source_sha256': '86c470d8d1f378c93e3c10763f4df59267b3b392f6404c26a34f0351fb193aa1',
              'source_type': 'nested_jar_lang',
              'source': 'minecraft/mods/balm-neoforge-26.1.2-26.1.2.13.jar',
              'archive_chain': [{'entry': 'META-INF/jarjar/kuma-api-neoforge-26.1.2.2.jar',
                                 'sha256': '95ea7006585360931ce4c6846d1234e81ed5e765cc234d0a4318d991ebe66abe'}],
              'namespace': 'kuma_api',
              'locale': 'ja_jp',
              'catalog_source_id': '3d88fa423967887f252a260981711da259561217c2ad1af0a24330e61fa5e8d8'},
 'quarryplus': {'version': '26.12.160',
                'jar_sha256': '905b0c1ea644923cf97a8c55a5187233214ca274371a066439fd5a56ed0056e8',
                'jar_entry': 'assets/quarryplus/lang/en_us.json',
                'source_sha256': 'd5546c7c9c155ab626ada1852d1a70fee4f6b3e03280db467dbe93a7c3883de1'},
 'apollib': {'version': '1.1.6',
             'source_type': 'nested_jar_lang',
             'source': 'minecraft/mods/lithostitched-1.8.0+beta6-neoforge-26.1.jar',
             'jar_sha256': 'ccb6692e30fba3e8cd88d58396d81053b455000b576f15b5e5fb00a24a1d8a3f',
             'archive_chain': [{'entry': 'META-INF/jarjar/apollib-1.1.6-neoforge-26.1.jar',
                                'sha256': '565434f421a15d0c4eb4bfca1c646329c015f86aeda90501d4979f435a11a39e'}],
             'jar_entry': 'assets/apollib/lang/en_us.json',
             'source_sha256': 'b4c80cb60c370bd77bed5ff5eac4b24e218f31c63f006316ba385bd7f38ddd75',
             'namespace': 'apollib',
             'locale': 'ja_jp',
             'catalog_source_id': '4f3afc5bd41b764394c693646d1b319748d626aad3a6734787380574065abd8d'},
 'enderio': {'version': '9.0.5-alpha',
             'source_type': 'nested_jar_lang',
             'source': 'minecraft/mods/enderio-9.0.5-alpha.jar',
             'jar_sha256': '4f85d88bbc0db379d8b8de8c5fdf18d0e552ef438feedcf8331dcf2ef54e1929',
             'archive_chain': [{'entry': 'META-INF/jarjar/com.enderio.enderio-modded-conduits-9.0.5-alpha.jar',
                                'sha256': '82cbd13953a91933768e22f77754820bf78b64db2b57bf38ab7f74b1a8fe61f1'}],
             'jar_entry': 'assets/enderio/lang/en_us.json',
             'source_sha256': 'dab0a712bbd62265c1e9af91e1049ec4bb997c91180ec27d311f25077c0dbbc0',
             'namespace': 'enderio',
             'locale': 'ja_jp',
             'catalog_source_id': '00483ca34ce6de5bb9157dab5b0c931ea6dd6b63fbceabcd9eba8f2f78f7dfe2'},
 'magicparticleslib': {'version': '1.4.0',
                       'source_type': 'nested_jar_lang',
                       'source': 'minecraft/mods/theurgy-26.1.2-neoforge-1.114.0.jar',
                       'jar_sha256': '874c46d9cc5075b01d7e1b06485b7e2ad1e53adea6bdc270efeeaec3934bedfa',
                       'archive_chain': [{'entry': 'META-INF/jarjar/magicparticleslib-26.1.2-neoforge-1.4.0.jar',
                                          'sha256': 'f3f4bc06d7df185427e2cc9943ff644a088900a52f723543b6638adbe27f9ac8'}],
                       'jar_entry': 'assets/magicparticleslib/lang/en_us.json',
                       'source_sha256': 'b199308dbb7ee42194789852090099e168dfc0a51022bd7e484ac4bc917d9d65',
                       'namespace': 'magicparticleslib',
                       'locale': 'ja_jp',
                       'catalog_source_id': '7953948d057071bc681d9a944a2917af52472bb4b548363a469af15f593dbd22'},
 'spectrelib': {'version': '0.21.0+26.1.2',
                'source_type': 'nested_jar_lang',
                'source': 'minecraft/mods/comforts-neoforge-15.0.0+26.1.2.jar',
                'jar_sha256': '23b7a63b3729dc590174ca0ca5740c22ddc93718ead6fa579a921d3e7fa5ac83',
                'archive_chain': [{'entry': 'META-INF/jarjar/spectrelib-neoforge-0.21.0+26.1.2.jar',
                                   'sha256': '4b85c10c81f53e7c12978137ef77b71c39b14bde392bd120978934e65311366f'}],
                'jar_entry': 'assets/spectrelib/lang/en_us.json',
                'source_sha256': '9708a0bf7fefae32049dcd9af2ecd276ab35d01db65877fc22dbcc2031bed8ed',
                'namespace': 'spectrelib',
                'locale': 'ja_jp',
                'catalog_source_id': '5433924ad5d96615f64114ec0258f97aeb6e465917696e0af9352312cf189f58'},
 'advanced_ae': {'version': '26.1.7',
                 'jar_sha256': 'fae810b62ecd1746ab9b74ba6e0b5242ab7c0e92d291704e4ea755c83230b233',
                 'jar_entry': 'assets/advanced_ae/lang/en_us.json',
                 'source_sha256': '5e51d65570442553dc00fe35d4fec9a2f9083a4fd519ca344692125238cb032e'},
 'extendedae': {'version': '26.1-1.0.4-neoforge',
                'jar_sha256': '0201b58f5bdd33b2edffc786fbea7fbdbae06861f5beea1e6144ce4774e66e21',
                'jar_entry': 'assets/extendedae/lang/en_us.json',
                'source_sha256': 'e179f160074aa4d920d915ae407361f52a95f2488879a521c6f2215916361915'}}
KEY_SETS = {'transmog': (25, 'b369562a850d8b4f2fdf4c3065d0582904bc886a63b675b92e4f6f08c81562ff'),
 'jei': (335, 'd937bcace1710a07a4c1a156d35b1f4046f9663ab67f9b8e534ce6c87e5a2907'),
 'appleskin': (22, '69aad68d780252788180e59a29c4e3a4457f47fc29ad3a2cf920ac1fb4ae332c'),
 'controlling': (12, 'bd5a753a17d7eb4acf894cf43b58d4a4c3f7b25a35f18e754d839c18d18207b1'),
 'jade': (496, '2abacb74df2a08a3058933548c1bb1418fe401c8c62f4338a409cedf3852cb44'),
 'searchables': (2, 'b897804392acbe7e4160dfcb321d51970637690d2830640a75c35bca9e87cc0e'),
 'resourcefulconfig': (32, 'd599c4e7fabeac66b14d77b9a8a9cd70a8209edc3a93f6eb16e42fa5be79f1d2'),
 'ae2netanalyser': (38, 'aa51ab5a9986cbfb47e635637baad22e68291bbf778f332b19fb2cee393bf30e'),
 'cumulus_menus': (35, '72ac5f03af805e3bdd88450fb66650f753ff71edcb93fe6273cfdf3bae1856d9'),
 'sodium': (105, 'd3d280e364521c640fc551a85233b94a01c6e95ad4579b6c68c8dba85b864464'),
 'betteradvancements': (3, '5145441ad0d99e9b99bc9ac9d4533768ccbe0ca5c819c5cc5d6f11c70afe1657'),
 'codedefinedgui': (63, 'f7fd0a8e553dd1b3f5344d5cff0f5018ca3cd2292e2013eeec9824cb044b68e7'),
 'sathlib': (18, '1718daf373b2466e0428b5fa85e32e9f59b188ce9af6ad62babed77299c928af'),
 'ae2addonlib': (11, '498a9170de17646759b0cad54bd36a103212976637e01380449c9f1dac0f03eb'),
 'ae2wtlib_api': (5, 'dca05b5cdc9225343dc9ccf8b99b7bb82630da60890e556f8e82854f83d2f1a6'),
 'kuma_api': (4, '022ec815d7d092142f437d2ea534c47d96c61da976b90e77c627aa38a2338028'),
 'quarryplus': (240, '19eb1e38cc705e91c97e9a69f16022d25606b9dddd84eacc355d815e4a5386ae'),
 'apollib': (7, '746f7cc9c49a69969dfd03af7be65c8023df6c8ba4f097fd37693ef71d91bced'),
 'enderio': (1, 'afe1b8102499b70c49e209a79bf72e5ad0c7d5df9af73d71bcf62cb41bc67960'),
 'magicparticleslib': (2, '3e0e053f7741f2238a3a75c47518047524cf2114caefae6aaaf382fd1fa75635'),
 'spectrelib': (1, 'e468fbd829e841aec05cf72412d7470d806a74817acfc3bec0f5beb9dcf2e16b'),
 'advanced_ae': (245, 'db020a473aba0ed24a3498b219d75f5ad47a49ac069fecc139407ca8bae53774'),
 'extendedae': (253, '617a9617e002fa13ed9e1f469a05c68e4ac5b0d8c088f56081fe5123edee07c2')}
PRESERVED_METADATA_KEYS = {'transmog': [],
 'jei': ['_comment'],
 'appleskin': [],
 'controlling': [],
 'jade': ['__comment', 'jade.metadata'],
 'searchables': [],
 'resourcefulconfig': [],
 'ae2netanalyser': [],
 'cumulus_menus': [],
 'sodium': [],
 'betteradvancements': [],
 'quarryplus': ['_comment'],
 'codedefinedgui': [],
 'sathlib': [],
 'ae2addonlib': [],
 'ae2wtlib_api': [],
 'kuma_api': [],
 'apollib': [],
 'enderio': [],
 'magicparticleslib': [],
 'spectrelib': [],
 'advanced_ae': [],
 'extendedae': []}
LICENSES = {'LICENSES/Project-MIT.txt': '14e77f04a42df608a6346aeacb757acf56aaba69450ff1dbf4b1e0fed3bbc08c',
 'LICENSES/Transmog-MIT.txt': 'a366506974a46752dbf54c187288b5d5de7f4570422b0cbacd4f5cd1dcb8f099',
 'LICENSES/JEI-MIT.txt': '108c93a97f3011c196b8226f5019a9c09ade318fe3a802be2f7f5ddb2c3a0d04',
 'LICENSES/AppleSkin-Unlicense.txt': '88d9b4eb60579c191ec391ca04c16130572d7eedc4a86daa58bf28c6e14c9bcd',
 'LICENSES/Controlling-MIT.txt': 'bd03ec3e3879605835ea5239cb6304b0d5694074d924b050c7099acbb89a5813',
 'LICENSES/Jade-CC-BY-NC-SA-4.0.md': '03d7d5b3f4b37a576d52db87542ac248e161fc47412192e9543c6a71a82b0ff3',
 'LICENSES/Searchables-MIT.txt': '3e8e9a2f792e603fea1bdcf62d1ef51c8b21090db2b1546c254315661ea1fef2',
 'LICENSES/ResourcefulConfig-MIT.txt': 'a8e7410d85c405cab5d1a51e198e51495c2ca6447b509eec540cfaff80bba8ea',
 'LICENSES/AE2NetworkAnalyzer-LGPL-3.0.txt': 'e3a994d82e644b03a792a930f574002658412f62407f5fee083f2555c5f23118',
 'LICENSES/CumulusMenus-LGPL-3.0.txt': 'e3a994d82e644b03a792a930f574002658412f62407f5fee083f2555c5f23118',
 'LICENSES/GPL-3.0.txt': '3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986',
 'LICENSES/Sodium-PolyForm-Shield-1.0.0.md': '67530f8e9adfcc5d2e9d72b804500cebb7472ff84c34a6729a80a2a9be901ee6',
 'LICENSES/BetterAdvancements-Dont-Be-a-Jerk.md': '5629128d1f6d0eeec510074078e63a5478f3460dca879bd56d44e41e02da29be',
 'LICENSES/QuarryPlus-LGPL-3.0.txt': 'da7eabb7bafdf7d3ae5e9f223aa5bdc1eece45ac569dc21b3b037520b4464768',
 'LICENSES/SathLib-LGPL-3.0.txt': '826710ee86ab3e3b6b6fb9ca1f7a107ff19210628a0cd183c52bf2a36e612d02',
 'LICENSES/AE2WTLib-API-MIT.txt': 'd61e8472fd606169227d467eae0fc46341256dc54ed05837df050b29ad0297ba',
 'LICENSES/Kuma-API-MIT.txt': '8535dbd4d6eee07c9da3d51be03b4ca20dff6fcb4aa9b8678abbfd41013242a8',
 'LICENSES/CC-BY-4.0.txt': 'd557539df68e771cc1eedcc91d13f70fca930e508d11eedcafa4b15db49e3744',
 'LICENSES/Apollib-MIT.txt': '2695dd4f7f3ef1ef7c13c84a46562c75959c56f3aa48eec2ed77da8a8644376f',
 'LICENSES/EnderIO-Unlicense.txt': 'ca2abdf695884c77ea4b4a5b64ca7b732d9d9dbade4eebc1c2e76c53e9e3bc83',
 'LICENSES/CC0-1.0.txt': 'a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499',
 'LICENSES/MagicParticlesLib-MIT-Code.txt': 'b05785f9f18e6716bab63424b11454513b9943a222595b70411009202fc592b5',
 'LICENSES/SpectreLib-Original-Notice.txt': '0c32ff90345592abc45b827a582a6cb0911accefe9cb3c9342c388e1e5cef458',
 'LICENSES/GNU-LGPL-2.1.txt': '5749785c8bdefafcb5d798270ed0a967036fe2ca63dcedade1627565dfef81d2',
 'LICENSES/AdvancedAE-LGPL-3.0.md': 'dfd18396dbca8237050f4c2cd9295c1a01a1c5ae78d17829e55842508a2c7f77',
 'LICENSES/ExtendedAE-LGPL-3.0.txt': 'e3a994d82e644b03a792a930f574002658412f62407f5fee083f2555c5f23118'}
NAMESPACE_LICENSES = {'transmog': ('LICENSES/Transmog-MIT.txt',),
 'jei': ('LICENSES/JEI-MIT.txt',),
 'appleskin': ('LICENSES/AppleSkin-Unlicense.txt',),
 'controlling': ('LICENSES/Controlling-MIT.txt',),
 'jade': ('LICENSES/Jade-CC-BY-NC-SA-4.0.md',),
 'searchables': ('LICENSES/Searchables-MIT.txt',),
 'resourcefulconfig': ('LICENSES/ResourcefulConfig-MIT.txt',),
 'ae2netanalyser': ('LICENSES/AE2NetworkAnalyzer-LGPL-3.0.txt', 'LICENSES/GPL-3.0.txt'),
 'cumulus_menus': ('LICENSES/CumulusMenus-LGPL-3.0.txt', 'LICENSES/GPL-3.0.txt'),
 'sodium': ('LICENSES/Sodium-PolyForm-Shield-1.0.0.md',),
 'betteradvancements': ('LICENSES/BetterAdvancements-Dont-Be-a-Jerk.md',),
 'quarryplus': ('LICENSES/QuarryPlus-LGPL-3.0.txt', 'LICENSES/GPL-3.0.txt'),
 'codedefinedgui': ('LICENSES/CC-BY-4.0.txt',),
 'sathlib': ('LICENSES/SathLib-LGPL-3.0.txt', 'LICENSES/GPL-3.0.txt'),
 'ae2addonlib': ('LICENSES/GPL-3.0.txt',),
 'ae2wtlib_api': ('LICENSES/AE2WTLib-API-MIT.txt',),
 'kuma_api': ('LICENSES/Kuma-API-MIT.txt',),
 'apollib': ('LICENSES/Apollib-MIT.txt',),
 'enderio': ('LICENSES/EnderIO-Unlicense.txt', 'LICENSES/CC0-1.0.txt'),
 'magicparticleslib': ('LICENSES/CC-BY-4.0.txt', 'LICENSES/MagicParticlesLib-MIT-Code.txt'),
 'spectrelib': ('LICENSES/SpectreLib-Original-Notice.txt', 'LICENSES/GNU-LGPL-2.1.txt'),
 'advanced_ae': ('LICENSES/AdvancedAE-LGPL-3.0.md', 'LICENSES/GPL-3.0.txt'),
 'extendedae': ('LICENSES/ExtendedAE-LGPL-3.0.txt', 'LICENSES/GPL-3.0.txt')}
PACKAGES = {'collection': {'directory': 'resourcepack',
                'release': 'release.json',
                'notice': 'NOTICE.md',
                'filename': 'ATM11-Japanese-0.6.0.zip',
                'namespaces': ('transmog',
                               'jei',
                               'appleskin',
                               'controlling',
                               'jade',
                               'searchables',
                               'resourcefulconfig',
                               'ae2netanalyser',
                               'cumulus_menus',
                               'sodium',
                               'betteradvancements',
                               'codedefinedgui',
                               'sathlib',
                               'ae2addonlib',
                               'ae2wtlib_api',
                               'kuma_api',
                               'quarryplus',
                               'apollib',
                               'enderio',
                               'magicparticleslib',
                               'spectrelib',
                               'advanced_ae',
                               'extendedae'),
                'licenses': ('LICENSES/Project-MIT.txt',
                             'LICENSES/Transmog-MIT.txt',
                             'LICENSES/JEI-MIT.txt',
                             'LICENSES/AppleSkin-Unlicense.txt',
                             'LICENSES/Controlling-MIT.txt',
                             'LICENSES/Jade-CC-BY-NC-SA-4.0.md',
                             'LICENSES/Searchables-MIT.txt',
                             'LICENSES/ResourcefulConfig-MIT.txt',
                             'LICENSES/AE2NetworkAnalyzer-LGPL-3.0.txt',
                             'LICENSES/CumulusMenus-LGPL-3.0.txt',
                             'LICENSES/GPL-3.0.txt',
                             'LICENSES/Sodium-PolyForm-Shield-1.0.0.md',
                             'LICENSES/BetterAdvancements-Dont-Be-a-Jerk.md',
                             'LICENSES/QuarryPlus-LGPL-3.0.txt',
                             'LICENSES/SathLib-LGPL-3.0.txt',
                             'LICENSES/AE2WTLib-API-MIT.txt',
                             'LICENSES/Kuma-API-MIT.txt',
                             'LICENSES/CC-BY-4.0.txt',
                             'LICENSES/Apollib-MIT.txt',
                             'LICENSES/EnderIO-Unlicense.txt',
                             'LICENSES/CC0-1.0.txt',
                             'LICENSES/MagicParticlesLib-MIT-Code.txt',
                             'LICENSES/SpectreLib-Original-Notice.txt',
                             'LICENSES/GNU-LGPL-2.1.txt',
                             'LICENSES/AdvancedAE-LGPL-3.0.md',
                             'LICENSES/ExtendedAE-LGPL-3.0.txt'),
                'pack': {'pack': {'description': 'ATM11 日本語改善 0.6.0: 23 namespaces / 1955 keys',
                                  'min_format': [84, 0],
                                  'max_format': [84, 0]},
                         'filter': {'block': [{'namespace': '^transmog$', 'path': '^lang/ja_jp\\.json$'}]}}}}
JEI_METADATA_VALUE = 'Debug (for a debug mode, do not need translation)'
# The whole original JAR is pinned above. This is the original JA runtime setting,
# not the English metadata or prose. No source JAR is needed to rebuild this pack.
JADE_ORIGINAL_JA_SHA256 = '381f227a22a7eb5cbf69c864752bd4fe72ea00f77ceed54df6b57b48550ba6b7'
JADE_METADATA_VALUE_SHA256 = 'e3cf5492749f2d1c3f333017f1aa6094138d2b02cd308c41432e25e2c51ad89a'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_file(root, name):
    path = root / name
    for part in (path, *path.parents):
        if part == root:
            break
        require(not part.is_symlink(), f'Symlink is not allowed: {name}')
    return path.read_bytes()


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs)


def valid_hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def validate_nested_identity(namespace, source):
    """Recheck the public nested identity without requiring private JARs to rebuild."""
    if 'archive_chain' not in POLICIES[namespace]:
        return  # Flat schema 1 remains byte-compatible with earlier public evidence.
    require(source['source_type'] == 'nested_jar_lang' and source['namespace'] == namespace and
            source['locale'] == 'ja_jp' and source['jar_entry'] == f'assets/{namespace}/lang/en_us.json',
            f'{namespace}: Wrong nested source kind/namespace/member')
    core = {key: value for key, value in source.items() if key not in {'version', 'catalog_source_id'}}
    identity_hash = digest(json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))
    require(identity_hash == source['catalog_source_id'], f'{namespace}: Nested parent/chain identity digest differs')


def validate_evidence(raw, namespace, language, language_sha256):
    evidence = parse(raw)
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'namespace', 'source', 'language_sha256', 'reviews',
    } and type(evidence['schema_version']) is int and evidence['schema_version'] == (2 if 'archive_chain' in POLICIES[namespace] else 1), f'{namespace}: Unexpected review evidence schema')
    require(evidence['namespace'] == namespace and evidence['source'] == POLICIES[namespace],
            f'{namespace}: Review source/version/hash does not match the pinned MOD')
    validate_nested_identity(namespace, evidence['source'])
    require(evidence['language_sha256'] == language_sha256, f'{namespace}: Review evidence language hash mismatch')
    reviews = evidence['reviews']
    require(isinstance(reviews, list) and bool(reviews), f'{namespace}: No independent review evidence')
    accepted, seen_reviews, seen_batches = set(), set(), set()
    for review in reviews:
        require(isinstance(review, dict) and set(review) == {
            'batch_id', 'review_sha256', 'submission_sha256', 'reviewer', 'decision', 'accepted_keys',
        }, f'{namespace}: Unexpected review record schema')
        batch = review['batch_id']
        require(isinstance(batch, str) and re.fullmatch('[A-Za-z0-9_.+-]+', batch) and batch not in seen_batches,
                f'{namespace}: Invalid/duplicate review batch')
        seen_batches.add(batch)
        require(valid_hash(review['review_sha256']) and valid_hash(review['submission_sha256']),
                f'{namespace}: Missing review/submission SHA-256')
        require(review['review_sha256'] not in seen_reviews, f'{namespace}: Duplicate independent review')
        seen_reviews.add(review['review_sha256'])
        reviewer = review['reviewer']
        require(isinstance(reviewer, dict) and set(reviewer) == {'agent', 'model'} and
                all(isinstance(v, str) and v.strip() for v in reviewer.values()), f'{namespace}: Missing reviewer identity')
        require(isinstance(review['decision'], str) and review['decision'] in {'accepted', 'partial'}, f'{namespace}: Review does not accept keys')
        keys = review['accepted_keys']
        require(isinstance(keys, list) and bool(keys) and all(isinstance(k, str) for k in keys) and
                len(keys) == len(set(keys)), f'{namespace}: Invalid/duplicate accepted keys')
        require(not accepted.intersection(keys), f'{namespace}: Overlapping review key assignments')
        accepted.update(keys)
    require(accepted == set(language), f'{namespace}: Language keys must exactly match the independently accepted key union')


def validated_files(root, package='collection'):
    config = PACKAGES[package]
    release_raw = read_file(root, config['release'])
    release = parse(release_raw)
    require(isinstance(release, dict) and set(release) == {'schema_version', 'version', 'review_status', 'languages'} and
            type(release['schema_version']) is int and release['schema_version'] == 3,
            'Unexpected release manifest schema')
    require(release['review_status'] == 'accepted', 'Independent language review is pending; no ZIP generated')
    require(release['version'] == VERSION, 'This builder prepares version 0.6.0; earlier releases remain immutable')
    require(isinstance(release['languages'], dict) and set(release['languages']) == set(config['namespaces']),
            f'{package}: Only the fixed package namespaces are permitted')
    directory = config['directory']
    pack_raw = read_file(root, directory + '/pack.mcmeta')
    require(json.dumps(parse(pack_raw), sort_keys=True, ensure_ascii=False) ==
            json.dumps(config['pack'], sort_keys=True, ensure_ascii=False),
            f'{package}: Pack metadata/filter differs from the fixed policy')
    files = {'pack.mcmeta': pack_raw, 'release.json': release_raw,
             'README.md': read_file(root, 'README.md'), 'NOTICE.md': read_file(root, config['notice'])}
    allowed_pack_files = {'pack.mcmeta'}
    for namespace, record in release['languages'].items():
        require(isinstance(record, dict) and set(record) == {
            'language_sha256', 'key_count', 'preserved_metadata_keys', 'review_evidence_sha256',
        }, f'{namespace}: Unexpected language release record')
        require(valid_hash(record['language_sha256']) and valid_hash(record['review_evidence_sha256']),
                f'{namespace}: Missing language/review evidence SHA-256')
        name = f'assets/{namespace}/lang/ja_jp.json'
        language_raw = read_file(root, directory + '/' + name)
        require(digest(language_raw) == record['language_sha256'], f'{namespace}: Language bytes changed after review')
        language = parse(language_raw)
        require(isinstance(language, dict) and bool(language) and all(isinstance(v, str) and v.strip() for v in language.values()),
                f'{namespace}: Every language value must be a nonempty string')
        expected_count, expected_keys_hash = KEY_SETS[namespace]
        keys_hash = digest(json.dumps(sorted(language), ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
        require(len(language) == expected_count and keys_hash == expected_keys_hash,
                f'{namespace}: All and only the exact source keys are required')
        require(type(record['key_count']) is int and record['key_count'] == len(language), f'{namespace}: Key count mismatch')
        require(record['preserved_metadata_keys'] == PRESERVED_METADATA_KEYS[namespace],
                f'{namespace}: Preserved metadata classification changed')
        if namespace == 'jei':
            require(language['_comment'] == JEI_METADATA_VALUE, 'JEI metadata must remain verbatim')
        if namespace == 'quarryplus':
            require(language['_comment'] == 'English lang file.', 'QuarryPlus metadata must remain verbatim')
        if namespace == 'jade':
            require(language['__comment'] == 'Only for testing:', 'Jade testing metadata must remain verbatim')
            require(digest(language['jade.metadata'].encode('utf-8')) == JADE_METADATA_VALUE_SHA256,
                    'Jade functional settings must match the pinned original Japanese value')
        evidence_name = f'reviews/{namespace}.json'
        evidence_raw = read_file(root, evidence_name)
        require(digest(evidence_raw) == record['review_evidence_sha256'], f'{namespace}: Review evidence bytes changed')
        validate_evidence(evidence_raw, namespace, language, record['language_sha256'])
        files[name], files[evidence_name] = language_raw, evidence_raw
        allowed_pack_files.add(name)
    pack_files = set()
    for path in (root / directory).rglob('*'):
        require(not path.is_symlink(), 'Resource pack contains a symlink')
        if path.is_file():
            pack_files.add(str(path.relative_to(root / directory)))
    require(pack_files == allowed_pack_files, 'Unexpected file in resourcepack; refusing to include it')
    require(set(NAMESPACE_LICENSES) == set(config['namespaces']), 'License scope differs from namespace allowlist')
    license_union = {'LICENSES/Project-MIT.txt'} | {name for names in NAMESPACE_LICENSES.values() for name in names}
    require(license_union == set(LICENSES) == set(config['licenses']), 'License allowlist does not match collection scopes')
    for name in config['licenses']:
        raw = read_file(root, name)
        require(digest(raw) == LICENSES[name], f'Upstream license bytes changed: {name}')
        files[name] = raw
    return release, files


def package_bytes(root, package='collection'):
    release, files = validated_files(root, package)
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, raw)
    return release['version'], output.getvalue()


def write_new_zip(directory, filename, raw):
    output = directory / filename
    if output.exists() or output.is_symlink():
        require(not output.is_symlink() and output.is_file() and output.read_bytes() == raw,
                'Existing release ZIP has different bytes; use a new version instead of overwriting it')
        return output
    fd, name = tempfile.mkstemp(prefix='.pack-', dir=directory)
    temporary = Path(name)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, output)
    finally:
        temporary.unlink()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate release inputs without producing a ZIP')
    args = parser.parse_args()
    selected = ('collection',)
    try:
        if args.check:
            for package in selected:
                validated_files(ROOT, package)
            print(f'RELEASE INPUTS OK: {VERSION}; {", ".join(selected)}; no ZIP generated')
            return 0
        # Validate and snapshot all selected inputs before producing any output.
        packages = [(PACKAGES[p]['filename'], package_bytes(ROOT, p)[1]) for p in selected]
        directory = ROOT / 'dist'
        require(not directory.is_symlink(), 'dist must not be a symlink')
        for filename, raw in packages:
            output = directory / filename
            if output.exists() or output.is_symlink():
                require(not output.is_symlink() and output.is_file() and output.read_bytes() == raw,
                        'Existing release ZIP differs; no selected ZIP was written')
        directory.mkdir(exist_ok=True)
        for filename, raw in packages:
            output = write_new_zip(directory, filename, raw)
            print(f'PACK OK: dist/{output.name}')
            print(f'SHA-256: {digest(raw)}')
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print(f'BUILD REFUSED: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
