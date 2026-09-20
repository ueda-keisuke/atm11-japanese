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
VERSION = '0.16.0'
NOTICE_SHA256 = '4597ea7b741868984c8a9696039f2c409eeb8ddd4ad2d1b3cb3186ab3b51fadf'
TRANSMOG_FILTER = {'block': [{'namespace': '^transmog$', 'path': '^lang/ja_jp\\.json$'}]}
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
                'source_sha256': 'e179f160074aa4d920d915ae407361f52a95f2488879a521c6f2215916361915'},
 'comforts': {'version': '15.0.0+26.1.2',
              'jar_sha256': '23b7a63b3729dc590174ca0ca5740c22ddc93718ead6fa579a921d3e7fa5ac83',
              'jar_entry': 'assets/comforts/lang/en_us.json',
              'source_sha256': '2e5684aa3ef4c81a71483f87aa7e3bc0cc506b60a85c65e617ccf2a9c22015a8'},
 'crafting_on_a_stick': {'version': '26.1-1.1',
                         'jar_sha256': '9dca3e70948d916cc3aa3f0dad78601158459022a657d30efeb0a805af97ca74',
                         'jar_entry': 'assets/crafting_on_a_stick/lang/en_us.json',
                         'source_sha256': 'c5b31af2e30db8265842ceb77c49864606687f32b88d9d6f05f6951e65cbafb0'},
 'toastcontrol': {'version': '26.1.2-10.0.0',
                  'jar_sha256': '49360b62f67194edac35342fc44d3413ae84392cafe341ba4de1ebac6fa95242',
                  'jar_entry': 'assets/toastcontrol/lang/en_us.json',
                  'source_sha256': '44bbd0c2ade0837af7320755e9b6f8ac2e8b80005ffecef5baa7dd9ef00aefb5'},
 'betteradvancedtooltips': {'version': '2601.1.0-build.9',
                            'jar_sha256': '1aef8ecc6f1b6c1952fed84c0302101019b2eb43c27d254152913b05a675143f',
                            'jar_entry': 'assets/betteradvancedtooltips/lang/en_us.json',
                            'source_sha256': '2b7e12c60a5ab2179773bc68a85747605c657eed02627197a2c4eca05f7a2f9e'},
 'toolbelt': {'version': '2.9.5',
              'jar_sha256': '5df697905865a66f681c7c0f74cc4c44e5ed1b03c1a5bf64901b25d6e9c439e2',
              'jar_entry': 'assets/toolbelt/lang/en_us.json',
              'source_sha256': 'ac5f07c4506f6069c2570402a8f70ebb37f2a61cdc2358355743e8049124a4f6'},
 'cucumber': {'version': '26.1.2-9.0.6',
              'jar_sha256': 'ad82d0a19f97086b8913029f2fbf10ad25ff591de4ac11e0776caa6dd1e8f9ed',
              'jar_entry': 'assets/cucumber/lang/en_us.json',
              'source_sha256': '40a6b16009febde352dce6a281eb8020923c3a271fdc1bb0f6f06eb877e03d0d'},
 'ironjetpacks': {'version': '9.0.3',
                  'sources': {'lang': {'jar_sha256': 'cf8df68bbde624ade6b47733c30c4b34faee1e6f26ead4220b77cf32de9b01f8',
                                       'jar_entry': 'assets/ironjetpacks/lang/en_us.json',
                                       'source_sha256': '1bb63988fb281ce7cd5db7c922bc14203f41a5ce0f5aefe76b14d9cffd15c43b',
                                       'source_type': 'jar_lang'},
                              'materials': {'jar_sha256': 'cf8df68bbde624ade6b47733c30c4b34faee1e6f26ead4220b77cf32de9b01f8',
                                            'jar_entry': 'com/blakebr0/ironjetpacks/registry/Jetpack.class',
                                            'source_sha256': 'df217f4269e0922d0a65d04e7bddd159a3f067287889a9090642082bbb09f9bb',
                                            'source_type': 'derived_jar_lang',
                                            'source_contract_sha256': 'c3e51fc6fd9ccbcd23c882ff08062b215bf718796bfc9ab0b885a8271af7da3d',
                                            'class_hashes': {'com/blakebr0/ironjetpacks/item/ComponentItem.class': 'cf7e80a4f06f241f4d452731a6437acedbc373d4a4a4c186ad44ecdbdf5c36c0',
                                                             'com/blakebr0/ironjetpacks/item/JetpackItem.class': '4685873695b62f46325b8663dd3e6605e588896cb4e7a366dc8a563e45ec18d6',
                                                             'com/blakebr0/ironjetpacks/registry/Jetpack.class': 'df217f4269e0922d0a65d04e7bddd159a3f067287889a9090642082bbb09f9bb'},
                                            'english_contract': [{'key': 'jetpack.bronze.name',
                                                                  'en': 'Bronze',
                                                                  'name': 'bronze'},
                                                                 {'key': 'jetpack.copper.name',
                                                                  'en': 'Copper',
                                                                  'name': 'copper'},
                                                                 {'key': 'jetpack.creative.name',
                                                                  'en': 'Creative',
                                                                  'name': 'creative'},
                                                                 {'key': 'jetpack.diamond.name',
                                                                  'en': 'Diamond',
                                                                  'name': 'diamond'},
                                                                 {'key': 'jetpack.electrum.name',
                                                                  'en': 'Electrum',
                                                                  'name': 'electrum'},
                                                                 {'key': 'jetpack.emerald.name',
                                                                  'en': 'Emerald',
                                                                  'name': 'emerald'},
                                                                 {'key': 'jetpack.gold.name',
                                                                  'en': 'Gold',
                                                                  'name': 'gold'},
                                                                 {'key': 'jetpack.invar.name',
                                                                  'en': 'Invar',
                                                                  'name': 'invar'},
                                                                 {'key': 'jetpack.iron.name',
                                                                  'en': 'Iron',
                                                                  'name': 'iron'},
                                                                 {'key': 'jetpack.platinum.name',
                                                                  'en': 'Platinum',
                                                                  'name': 'platinum'},
                                                                 {'key': 'jetpack.silver.name',
                                                                  'en': 'Silver',
                                                                  'name': 'silver'},
                                                                 {'key': 'jetpack.steel.name',
                                                                  'en': 'Steel',
                                                                  'name': 'steel'},
                                                                 {'key': 'jetpack.stone.name',
                                                                  'en': 'Stone',
                                                                  'name': 'stone'},
                                                                 {'key': 'jetpack.wood.name',
                                                                  'en': 'Wood',
                                                                  'name': 'wood'}]}}},
 'functionalstorage': {'version': '1.6.1',
                       'jar_sha256': 'cfd016afdc427f0ba6a3e11aad61112ee0458f43f32a33fa4f4fb576ea6c2254',
                       'jar_entry': 'assets/functionalstorage/lang/en_us.json',
                       'source_sha256': '2b1c7483a10a3711a4acbbd605b420b0acc90ab066e1bd5532402308d9b9591e'},
 'buildinggadgets2': {'version': '1.4.6',
                      'jar_sha256': '67c02d3a822ddd785692c581ae05b93a1b88767846bb6c89d20498b5598b72ca',
                      'jar_entry': 'assets/buildinggadgets2/lang/en_us.json',
                      'source_sha256': '799f2d4149bf78c56437bd903802f3c4368194f4a6d7b844a02bc9732df1f8fc'},
 'charginggadgets': {'version': '1.16.1',
                     'sources': {'lang': {'jar_sha256': 'ccdea206eed498468abd301af253785dc9ac2e6bd8294c5289a07023a948f7a1',
                                          'jar_entry': 'assets/charginggadgets/lang/en_us.json',
                                          'source_sha256': '8339631abc45e840c01fa7cbf5875256052ed5ebaa7af458c8fba1ae6141daa5',
                                          'source_type': 'jar_lang'},
                                 'configuration': {'jar_sha256': 'ccdea206eed498468abd301af253785dc9ac2e6bd8294c5289a07023a948f7a1',
                                                   'jar_entry': 'com/direwolf20/charginggadgets/Config$CategoryGeneral.class',
                                                   'source_sha256': 'a1785dd8559d71ff55c8f2b52e8786ebeaac337c320a4fe17258ecdaf8a51862',
                                                   'source_type': 'derived_jar_lang',
                                                   'source_contract_sha256': 'aa9cb0b458859ea19d116a02113ac73da6205ad281e5700b3182e2c1ccbd952e',
                                                   'class_hashes': {'com/direwolf20/charginggadgets/Config$CategoryGeneral.class': 'a1785dd8559d71ff55c8f2b52e8786ebeaac337c320a4fe17258ecdaf8a51862',
                                                                    'com/direwolf20/charginggadgets/Config.class': 'c82bcf76444a36e3f527ddd7ae335e7b5a5673161681e3ed8fdddda6f48f09f6'},
                                                   'english_contract': [{'key': 'charginggadgets.configuration.general',
                                                                         'en': 'charginggadgets.configuration.general',
                                                                         'name': 'general'},
                                                                        {'key': 'charginggadgets.configuration.general.tooltip',
                                                                         'en': 'General settings',
                                                                         'name': 'general'},
                                                                        {'key': 'charginggadgets.configuration.chargerMaxEnergy',
                                                                         'en': 'charginggadgets.configuration.chargerMaxEnergy',
                                                                         'name': 'chargerMaxEnergy'},
                                                                        {'key': 'charginggadgets.configuration.chargerMaxEnergy.tooltip',
                                                                         'en': 'Maximum power for the '
                                                                               'Charging Station\n'
                                                                               ' Default: 1000000',
                                                                         'name': 'chargerMaxEnergy'}],
                                                   'runtime_dependencies': {'neoforge': {'class_hashes': {'net/neoforged/neoforge/client/gui/ConfigurationScreen$ConfigurationSectionScreen.class': '5e7c94bf81f50a8395f2b9aefb3ddc2530d87cd914293b94f29da776a2a86aeb',
                                                                                                          'net/neoforged/neoforge/client/gui/ConfigurationScreen$TranslationChecker.class': '881f89a229127ddf3a484b7591e8131b6a54014361d3379a19bb7c1cf2ecda32',
                                                                                                          'net/neoforged/neoforge/client/gui/ConfigurationScreen.class': '283430e120dc0157d645189b544652e875b72bc2c312a0acfe975a8a326343e4',
                                                                                                          'net/neoforged/neoforge/common/ModConfigSpec$Builder.class': 'a9dc9214b2758279c74321d673e5568e2214f52cb23e0fc6d5f08bd0a5c6610b',
                                                                                                          'net/neoforged/neoforge/common/ModConfigSpec.class': '2070549e5f38a01747bd1e7e114f20a68c0813fe81f7bc65ee5cc5b90f4c0a4d'},
                                                                                         'jar_sha256': 'b37e097292d6631cf2ff6c3d6d1ad63dc9ce704eae198d49f1bd48baeb5e7776',
                                                                                         'maven_coordinate': 'net.neoforged:neoforge:26.1.2.106:universal',
                                                                                         'version': '26.1.2.106'}}}}},
 'curios': {'version': '15.0.0+26.1.2',
            'jar_sha256': 'ea1e92cd9dbfb93d2d363e2aced406a1749a4ed3e47bf06cce463903a99fd267',
            'jar_entry': 'assets/curios/lang/en_us.json',
            'source_sha256': '2915b2028e204f160d8f2d180aaf150996903c539548a6acadfa3aaabe394f68'},
 'naturescompass': {'version': '26.1-3.3.0-neoforge',
                    'jar_sha256': 'aa58cccc7c40230b75494d53fa21f008e0d76825c7881c5edbc59cf30abb79d5',
                    'jar_entry': 'assets/naturescompass/lang/en_us.json',
                    'source_sha256': '2312bf1655fb2bf8b0dd3fb27edd76659017d499c0a29190e39e2eab1759e9bd'},
 'simplebackups': {'version': '26.1.5',
                   'jar_sha256': '0b42165d9fc5381c4e99ae568deaa6728ba883f59a9f8fb37427fc7fd63b3b43',
                   'jar_entry': 'assets/simplebackups/lang/en_us.json',
                   'source_sha256': 'd19b811d572b077ae6d127be3d2fc94878a603cf470c2b85777482d0fe13f079'},
 'elevatorid': {'version': '26.1-1.16.2',
                'jar_sha256': 'f367a6eb009c595fa051368d61473a028fa7f3e1c76d55300a06ab546d3b1bad',
                'jar_entry': 'assets/elevatorid/lang/en_us.json',
                'source_sha256': 'a44258ae4164984f4a99f4688a448ac69d8dfa111dd89a8588fb167b5183da72'},
 'mysticalautomation': {'version': '2.0.6',
                        'jar_sha256': '439e00d8b33ecbd7eff71df8814f3d7dc797e87e36fdcd4f4c9f3e4980c6e1df',
                        'jar_entry': 'assets/mysticalautomation/lang/en_us.json',
                        'source_sha256': 'f41e095e8ba6fab1c2ede01948d1e5be082169f171460490dc9e315092dda2bb'},
 'neoforge': {'version': '26.1.2.106',
              'jar_sha256': 'b37e097292d6631cf2ff6c3d6d1ad63dc9ce704eae198d49f1bd48baeb5e7776',
              'jar_entry': 'assets/neoforge/lang/en_us.json',
              'source_sha256': '0de53ccd56b413c56aab33292618709e936360985c749623783121dab49cbad6',
              'source_type': 'runtime_jar_lang',
              'source_contract_sha256': 'dc0e107016382faffd4c49a632b0f3a3a821a498b94917cd0c8b4198e69ad45f',
              'namespace': 'neoforge',
              'locale': 'ja_jp',
              'runtime_artifact': {'maven_coordinate': 'net.neoforged:neoforge:26.1.2.106:universal',
                                   'version': '26.1.2.106',
                                   'jar_sha256': 'b37e097292d6631cf2ff6c3d6d1ad63dc9ce704eae198d49f1bd48baeb5e7776'},
              'scope_prefix': 'neoforge.configuration.'},
 'moreoverlays': {'version': '1.24.4',
                  'jar_sha256': 'c493dc1570d008c5a9fb55466fc3b35b25a43d4250956a837365ea3648dc9df1',
                  'jar_entry': 'assets/moreoverlays/lang/en_us.json',
                  'source_sha256': 'f6c8ec1067f04b3db1ca5ef560ea6b135358266bf5035cd31e16f8c02d25d946'},
 'interdimensionalwirelesstransmitter': {'version': '26.1.2-1.0.1',
                                         'jar_sha256': '9466a3992f0f27cc1faf0f560c260e1e5741d27977fe4f032ac7079f15f7a01b',
                                         'jar_entry': 'assets/interdimensionalwirelesstransmitter/lang/en_us.json',
                                         'source_sha256': '9f766ecb36ed67d014bbff30741bd8ea3c9e1aaea901de0d43b6ba6c771bee18'},
 'enchdesc': {'version': '26.1.2.6',
              'jar_sha256': 'cc86e80d23fb771097441dee77be5d971b4955cafa604690e61cc010083e5dd8',
              'jar_entry': 'assets/enchdesc/lang/en_us.json',
              'source_sha256': 'ff1e03874d39f9e3011bf30afc3e88b754a9b3544470459c38b9b0603faf3591'},
 'extremesoundmuffler': {'version': '4.03',
                         'jar_sha256': '5b44c2dad9b0e371748287fed299933dd58d015a42f0860d8c59d29d14764c77',
                         'jar_entry': 'assets/extremesoundmuffler/lang/en_us.json',
                         'source_sha256': '77dd7b0e7f33659e0e9bbd30eb7cb077403f4c70271f4309907bfa6513eaae93'},
 'sfm': {'version': '4.34.0',
         'jar_sha256': 'cace8809600cea007dbe5c73dc04c2f780375547ec0717a1ec8c25d991140bf1',
         'jar_entry': 'assets/sfm/lang/en_us.json',
         'source_sha256': '64189966cbcaf6714a4d56f0dcca9e057e70ce7a413fc466325d2bf1cdb0b090'},
 'dimstorage': {'version': '10.0.1',
                'jar_sha256': 'e6808c0fe40f671dd0625c9ab612fd75fe5453a528a58580f13c21a0b93c7511',
                'jar_entry': 'assets/dimstorage/lang/en_us.json',
                'source_sha256': '4713de32d6f9833840fad59f9f56b0f036715e5846270c5694c49b5f3c057eeb'},
 'stepcrafter': {'version': '26.1.2-1.0.3',
                 'jar_sha256': '78a5392cf562e75bf803937f6f41d28b51aba3c474e1c95f5aab5ec265abee30',
                 'jar_entry': 'assets/stepcrafter/lang/en_us.json',
                 'source_sha256': '2184445666a7b0571b923e0f090a8359e9153dfd2408f41c263a8ee71694c293'},
 'refinedstorage_quartz_arsenal': {'version': '2.0.6',
                                   'jar_sha256': '4e1bd12aa644320195553e76edbdb159150dd51db6268f532544206567ef165a',
                                   'jar_entry': 'assets/refinedstorage_quartz_arsenal/lang/en_us.json',
                                   'source_sha256': '83bb43ab5a611522ace3a4ac70f099a28c82b1a70fea3ab571dfffad84eb5f39'},
 'keybindbundles': {'version': '2.0.0',
                    'sources': {'lang': {'jar_sha256': '8e16eb32f49d55e7b106d6fd406bdd395d56ad0d04e9ffba3af0446e04d0078b',
                                         'jar_entry': 'assets/keybindbundles/lang/en_us.json',
                                         'source_sha256': '12c471f276b91698b06356a395275aaa02ddd49b46febd8e9e7610e90673da68',
                                         'source_type': 'jar_lang'},
                                'configuration': {'jar_sha256': '8e16eb32f49d55e7b106d6fd406bdd395d56ad0d04e9ffba3af0446e04d0078b',
                                                  'jar_entry': 'com/matyrobbrt/keybindbundles/KBClientConfig.class',
                                                  'source_sha256': 'a01b938891120f78b180b902b031dca93353b41ad25f7ab0c0253a1754f7afd1',
                                                  'source_type': 'derived_jar_lang',
                                                  'source_contract_sha256': '03b77faf4f3e3e4a7118c6517e175cf206a382af3d6831f82fe4b80118d184b3',
                                                  'class_hashes': {'com/matyrobbrt/keybindbundles/KBClientConfig.class': 'a01b938891120f78b180b902b031dca93353b41ad25f7ab0c0253a1754f7afd1',
                                                                   'com/matyrobbrt/keybindbundles/KeyBindBundleManager$RadialKeyMapping.class': 'cecd64f3059a979765cff68c8dff22bfcedf7f3979daff08267768e472d78d33',
                                                                   'com/matyrobbrt/keybindbundles/KeyBindBundleManager.class': '20c1afd304c82ff41ea6dc20b43e644b0aee23e459fb6d84384fd19853232d0e'},
                                                  'runtime_dependencies': {'neoforge': {'class_hashes': {'net/neoforged/neoforge/client/gui/ConfigurationScreen$ConfigurationSectionScreen.class': '5e7c94bf81f50a8395f2b9aefb3ddc2530d87cd914293b94f29da776a2a86aeb',
                                                                                                         'net/neoforged/neoforge/client/gui/ConfigurationScreen$TranslationChecker.class': '881f89a229127ddf3a484b7591e8131b6a54014361d3379a19bb7c1cf2ecda32',
                                                                                                         'net/neoforged/neoforge/client/gui/ConfigurationScreen.class': '283430e120dc0157d645189b544652e875b72bc2c312a0acfe975a8a326343e4',
                                                                                                         'net/neoforged/neoforge/common/ModConfigSpec$Builder.class': 'a9dc9214b2758279c74321d673e5568e2214f52cb23e0fc6d5f08bd0a5c6610b',
                                                                                                         'net/neoforged/neoforge/common/ModConfigSpec.class': '2070549e5f38a01747bd1e7e114f20a68c0813fe81f7bc65ee5cc5b90f4c0a4d'},
                                                                                        'jar_sha256': 'b37e097292d6631cf2ff6c3d6d1ad63dc9ce704eae198d49f1bd48baeb5e7776',
                                                                                        'maven_coordinate': 'net.neoforged:neoforge:26.1.2.106:universal',
                                                                                        'version': '26.1.2.106'}},
                                                  'english_contract': [{'key': 'keybindbundles.configuration.clipMouseToMenu.tooltip',
                                                                        'en': 'Set to true to clip the mouse '
                                                                              'within the bounds of the '
                                                                              'radial menu of bundles',
                                                                        'name': 'clipMouseToMenu'},
                                                                       {'key': 'keybindbundles.configuration.triggerKeymappingOnRelease.tooltip',
                                                                        'en': 'If set to true, the '
                                                                              'keymapping hovered in a '
                                                                              'bundle menu will be '
                                                                              'automatically triggered '
                                                                              '(without needing a click) '
                                                                              'upon release of the bundle '
                                                                              'key',
                                                                        'name': 'triggerKeymappingOnRelease'},
                                                                       {'key': 'keybindbundles.configuration.ignoreInvalidKeyChecks.tooltip',
                                                                        'en': 'ONLY USE THIS IF YOU KNOW '
                                                                              "WHAT YOU'RE DOING\n"
                                                                              'Ignore invalid key checks in '
                                                                              'InputConstants#isKeyDown',
                                                                        'name': 'ignoreInvalidKeyChecks'}]}}},
 'inworldrecipes': {'version': '2.5.1',
                    'jar_sha256': '1fd0898a0e593368828e652be86857216e569479514893eae7233051d0d96876',
                    'jar_entry': 'assets/inworldrecipes/lang/en_us.json',
                    'source_sha256': '12ae6572529309fd0aa656c047657040d435a65e61f6475d543bd33af44c3e01'},
 'matc': {'version': '1.8.0',
          'jar_sha256': 'e38d08da7a43249d281dbc4aabae37cca59e980a925c4a52f5a830950386c777',
          'jar_entry': 'assets/matc/lang/en_us.json',
          'source_sha256': '112e94d9717a11e2db109f91724c53b44ce1cbc82ac805665397659a2ad9471d'},
 'ae2wtlib': {'version': '26.1.1-beta',
              'jar_sha256': '9309564ee5f3640ddbcc55450e0727e5a7790488f3b82af350d3012960b18311',
              'jar_entry': 'assets/ae2wtlib/lang/en_us.json',
              'source_sha256': 'aab41084febf12df6f99358a2bf51c1434107e133d6fda1f13445edba14ecd34'},
 'measurements': {'version': '4.0.0',
                  'jar_sha256': 'e72dadf160dce841d3c395138938eaee0ce09b9986bb7c1d5d3591c27752af11',
                  'jar_entry': 'assets/measurements/lang/en_us.json',
                  'source_sha256': '59ee60e9642c729a8f9458de17a739498d9574a7e9c59aa6a7bd06420143c2fe'}}
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
 'extendedae': (253, '617a9617e002fa13ed9e1f469a05c68e4ac5b0d8c088f56081fe5123edee07c2'),
 'comforts': (84, '8b7e5b99c3567710c38e3c018ce2403ad6fa90567c43f3afb30cbfc14836a631'),
 'crafting_on_a_stick': (14, 'dc7eb09f7d91088d2ab87c9cecfdca4099c91510c3c64406dc43ce1b18de1e81'),
 'toastcontrol': (2, '52d71e9e1e5d64b49ed5072bcb695885afbe469b612b6f63e6a53a7390a9a6c1'),
 'betteradvancedtooltips': (5, '2aa164afe03073e3b01048d93a8abc21365dba77310d9fadc9247720ad1f9094'),
 'toolbelt': (26, 'a6565085cec975fc3572244b15fff8999620d0b0bae9ab5fe5da3ae834ab1d38'),
 'cucumber': (16, '81383395782e852a51817af84ee8ef509aac51c605a324a8c47ecab80d0124cb'),
 'ironjetpacks': (55, '26847e092d60d1cdb6811364fa531fa3be736220baa74594ccda7ca8fe6fd92b'),
 'functionalstorage': (164, '5cb38a402b107fcdd1e571945061be664faac471f30f330a8ac6e5dcc77781f6'),
 'buildinggadgets2': (113, '86fa833b2f9490bac7e9be9a71410f45e143584d2bbc75b95151db02b4606dc1'),
 'charginggadgets': (10, '92c9170e8df5543283f8377a59f3aef7a63ee5dc709ed191b73a747f01119155'),
 'curios': (48, '48448bd37c4568fa7ea4a8abd4132ce112169de66c9f2c0a79fc50edbfad10a9'),
 'naturescompass': (44, '778e3d9cedd84969f9b5afc49b046a73c72ae72c4fa15875b33dd033c4e3d201'),
 'simplebackups': (43, '979b29e83d159105bfdeb7940003902c2de6ebbf8ecefc9c7b7057a191f026da'),
 'elevatorid': (29, 'f284bd5235b6e454a8c6c168b210b31e126a0ac206e116840c148dc3244dbc38'),
 'mysticalautomation': (42, '49b0b062ab7ac0b3c7bed6e7fb1e7f715977950a3a30611965d33d2b8cf97753'),
 'neoforge': (46, '0fb199c160060a593de5238cf97c8e02cd9096a36120a9c5ee6dff87c45aa454'),
 'moreoverlays': (40, '1618b941ba6d309322d6d68f6e0ecb81896fa8472f2afafc64f67d59856ea0b2'),
 'interdimensionalwirelesstransmitter': (10,
                                         '38101869dc9d8dfcb8bc0105ca74eb29f1e6ece367a962f285ff8005d9963b62'),
 'enchdesc': (183, '8f93f7f6d72674769987ed1d0c46cfc17eb9c0c8389c9b95a2e40cace11001dc'),
 'extremesoundmuffler': (93, 'ae57eb6617344d60e2c8c265c3033bf6c62103a62b0570f958419b60c083fdfb'),
 'sfm': (277, '12961d780fd822177c6d9f7a9e72520e1b289a6a798e9c60e8e894c4e349bc78'),
 'dimstorage': (36, 'e189469735447e92ccb27207644b6cc5493f7b6ab797816ffd4f6b8a2048fc10'),
 'stepcrafter': (80, 'd874eee788d8af8267292a7659b2dbab94a6c7b090bc162f7bef7af25ad864d1'),
 'refinedstorage_quartz_arsenal': (23, '3a0235d95e238a19fbd7e969fb24fbae3978ff9993b11efd21d91893abed3463'),
 'keybindbundles': (29, '10bfa2a54f7f09d3bab32337b976a4a5345dcef5d088a67cf1e7a35a8d4802a9'),
 'inworldrecipes': (38, 'fe114c770cfdc5a174e14fa805d0a53621c774706129215b45c43910d9c04597'),
 'matc': (40, '831e3f35c21e5bfd5d916edc6d49421f476c5f475d0742fe1a18197d93f27f83'),
 'ae2wtlib': (44, '0675310a8c56a6662d6e29447ff018f6c3ece14aac39bbfc1336474f3288aca4'),
 'measurements': (15, '756adfd29c6caff22cb93740fe22c53ce74baa9bb07583c70f71a18e90427ac0')}
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
 'extendedae': [],
 'comforts': [],
 'crafting_on_a_stick': [],
 'toastcontrol': [],
 'betteradvancedtooltips': [],
 'toolbelt': [],
 'cucumber': [],
 'ironjetpacks': [],
 'functionalstorage': [],
 'buildinggadgets2': [],
 'charginggadgets': [],
 'curios': [],
 'naturescompass': ['_comment'],
 'simplebackups': [],
 'elevatorid': [],
 'mysticalautomation': [],
 'neoforge': [],
 'moreoverlays': [],
 'interdimensionalwirelesstransmitter': [],
 'enchdesc': ['__comment_jei',
              '__support_betterarcheology',
              '__support_create_stuff',
              '__support_deeperdarker',
              '__support_dungeonsenchantments',
              '__support_endlessbiomes',
              '__support_gofish',
              '__support_grapplemod',
              '__support_hunterillager',
              '__support_improved_exp',
              '__support_shield+',
              '__support_stalwart_dungeons',
              '_comment'],
 'extremesoundmuffler': [],
 'sfm': [],
 'dimstorage': [],
 'stepcrafter': [],
 'refinedstorage_quartz_arsenal': [],
 'keybindbundles': [],
 'inworldrecipes': [],
 'matc': [],
 'ae2wtlib': [],
 'measurements': ['_comment']}
PROJECT_NOTICES = {'simplebackups': {'_comment': 'Modified by ATM11 Japanese project / ueda-keisuke on 2026-09-20: Japanese '
                               'language entries revised or supplied. Original project: Simple Backups by '
                               'MelanX; Apache-2.0. See NOTICE.md and '
                               'LICENSES/SimpleBackups-Apache-2.0.txt.'}}
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
 'LICENSES/ExtendedAE-LGPL-3.0.txt': 'e3a994d82e644b03a792a930f574002658412f62407f5fee083f2555c5f23118',
 'LICENSES/Comforts-LGPL-3.0-or-later.txt': '76673eefd330bf57418d1688204b38b33912546e698dfb8940b8dbb7e3d85770',
 'LICENSES/Comforts-COPYING.txt': '8b1ba204bb69a0ade2bfcf65ef294a920f6bb361b317dba43c7ef29d96332b9b',
 'LICENSES/Comforts-COPYING.LESSER.txt': 'e3a994d82e644b03a792a930f574002658412f62407f5fee083f2555c5f23118',
 'LICENSES/CraftingOnAStick-GPL-3.0.txt': '3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986',
 'LICENSES/ToastControl-MIT.txt': '418c2a244f332d6f802e3a8785aa3d431e05e42788ca49e60e214ca3beb02b1f',
 'LICENSES/BetterAdvancedTooltips-MIT.txt': '9edb55b1a18dd84104002f0299ce42f6bf3dbf10269e3e288c80e57db46d1b90',
 'LICENSES/ToolBelt-BSD-3-Clause.txt': 'fc522363d94e4b83668ead1e71a90fc89d8e4fc60f2263fa4162089783ef2c1b',
 'LICENSES/Cucumber-MIT.txt': 'b39f78eb5c0ea06ffd89f824925c86f712f27f663f976cd50727df6856f037a2',
 'LICENSES/IronJetpacks-MIT.txt': 'b39f78eb5c0ea06ffd89f824925c86f712f27f663f976cd50727df6856f037a2',
 'LICENSES/FunctionalStorage-MIT.txt': 'b64ac86da57a720bed3d42256d4ed88cfca541b22c3f3167e0ab86b689c0072a',
 'LICENSES/BuildingGadgets2-MIT.txt': '85c1d2f248062d5a9d86f408a95ff453cce2da66da9983f4f2264b4f080c379f',
 'LICENSES/ChargingGadgets-MIT.txt': '950d1ff370fd55e2dde8de824c0e2ed6cac7a656a7be9afc417b61ed6732347d',
 'LICENSES/Curios-LGPL-3.0-or-later.txt': '951a45e06788cc01755e42838b801eee5229ce6cbd2405eee434cbed67c36844',
 'LICENSES/Curios-COPYING.txt': '8b1ba204bb69a0ade2bfcf65ef294a920f6bb361b317dba43c7ef29d96332b9b',
 'LICENSES/Curios-COPYING.LESSER.txt': 'e3a994d82e644b03a792a930f574002658412f62407f5fee083f2555c5f23118',
 'LICENSES/NaturesCompass-CC-BY-NC-SA-4.0.md': 'f32903cdd6843cbaf3c150b6e4e03f73d2c7e717dbdedc26b6cb399141c0bad3',
 'LICENSES/SimpleBackups-Apache-2.0.txt': 'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30',
 'LICENSES/ElevatorID-MIT.txt': '5463250e11d1f9515c17a6563244f6bc63820c264400dedde321f54dd348e36b',
 'LICENSES/MysticalAutomation-MIT.txt': '99c858766d01eef611a38b234a2bba5ca9fa2c015e3c12c6da2f80fe3515341e',
 'LICENSES/NeoForge-LGPL-2.1.txt': 'a8746534d481c0d1046a1c6c02acc034231ad45b56f04ca35212e1f23e3f2712',
 'LICENSES/MoreOverlays-MIT.txt': '63ea7f78b45a1c18732a34d272b7dc6bc501e708386354b2dbdba68bc6e0b5de',
 'LICENSES/InterdimensionalWirelessTransmitter-MIT.txt': '132234f0de1d6bcd91e41a6b9d995d9022d1da093c2c94d131ba1adf4117fcc2',
 'LICENSES/EnchantmentDescriptions-LGPL-2.1.txt': 'a7bb85ecc913dadfba4cef7af27d2789094bdfb9e46d86b0cd8f917ba4e64e23',
 'LICENSES/ExtremeSoundMuffler-LGPL-3.0.txt': 'ca25c1e642be3f3fc0576de17a5003df44305d5282a5e0c6cf0999cc75438ec0',
 'LICENSES/SuperFactoryManager-MPL-2.0.txt': '1f256ecad192880510e84ad60474eab7589218784b9a50bc7ceee34c2b91f1d5',
 'LICENSES/DimStorage-AGPL-3.0.txt': '8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef',
 'LICENSES/StepCrafter-MIT.txt': '976da1a41c4b86061101f101832ac3d904d95c6836554f5a260c202338b5427d',
 'LICENSES/RefinedStorageQuartzArsenal-MIT.md': '4f332ed10b4b214c0397a37b0344aa5fd4517ea5631e580c6b43676f92ad9f4e',
 'LICENSES/KeyBindBundles-MIT.txt': '39b326c42567abc3d4273a67b062c3434fdfc7fa29a2b86a76f9cf41d30171d5',
 'LICENSES/InWorldRecipes-MIT.txt': '46daa0bbd05e4249dc930a44059f7abe1e4d36d8a355d8cb840fd190f6df430b',
 'LICENSES/MysticalAgricultureTieredCrystals-MIT.txt': '285d661d5a712ee320753bd6e33319bbc95ad947cf97c35844552d3817b070e1',
 'LICENSES/AE2WTLib-MIT.txt': 'd61e8472fd606169227d467eae0fc46341256dc54ed05837df050b29ad0297ba',
 'LICENSES/Measurements-MIT.txt': 'ded3792ee1ef728cec734993688f87ec6bf8cd050cdee99ed46613433becfa18'}
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
 'extendedae': ('LICENSES/ExtendedAE-LGPL-3.0.txt', 'LICENSES/GPL-3.0.txt'),
 'comforts': ('LICENSES/Comforts-LGPL-3.0-or-later.txt',
              'LICENSES/Comforts-COPYING.txt',
              'LICENSES/Comforts-COPYING.LESSER.txt'),
 'crafting_on_a_stick': ('LICENSES/CraftingOnAStick-GPL-3.0.txt',),
 'toastcontrol': ('LICENSES/ToastControl-MIT.txt',),
 'betteradvancedtooltips': ('LICENSES/BetterAdvancedTooltips-MIT.txt',),
 'toolbelt': ('LICENSES/ToolBelt-BSD-3-Clause.txt',),
 'cucumber': ('LICENSES/Cucumber-MIT.txt',),
 'ironjetpacks': ('LICENSES/IronJetpacks-MIT.txt',),
 'functionalstorage': ('LICENSES/FunctionalStorage-MIT.txt',),
 'buildinggadgets2': ('LICENSES/BuildingGadgets2-MIT.txt',),
 'charginggadgets': ('LICENSES/ChargingGadgets-MIT.txt',),
 'curios': ('LICENSES/Curios-LGPL-3.0-or-later.txt',
            'LICENSES/Curios-COPYING.txt',
            'LICENSES/Curios-COPYING.LESSER.txt'),
 'naturescompass': ('LICENSES/NaturesCompass-CC-BY-NC-SA-4.0.md',),
 'simplebackups': ('LICENSES/SimpleBackups-Apache-2.0.txt',),
 'elevatorid': ('LICENSES/ElevatorID-MIT.txt',),
 'mysticalautomation': ('LICENSES/MysticalAutomation-MIT.txt',),
 'neoforge': ('LICENSES/NeoForge-LGPL-2.1.txt',),
 'moreoverlays': ('LICENSES/MoreOverlays-MIT.txt',),
 'interdimensionalwirelesstransmitter': ('LICENSES/InterdimensionalWirelessTransmitter-MIT.txt',),
 'enchdesc': ('LICENSES/EnchantmentDescriptions-LGPL-2.1.txt',),
 'extremesoundmuffler': ('LICENSES/ExtremeSoundMuffler-LGPL-3.0.txt', 'LICENSES/GPL-3.0.txt'),
 'sfm': ('LICENSES/SuperFactoryManager-MPL-2.0.txt',),
 'dimstorage': ('LICENSES/DimStorage-AGPL-3.0.txt',),
 'stepcrafter': ('LICENSES/StepCrafter-MIT.txt',),
 'refinedstorage_quartz_arsenal': ('LICENSES/RefinedStorageQuartzArsenal-MIT.md',),
 'keybindbundles': ('LICENSES/KeyBindBundles-MIT.txt',),
 'inworldrecipes': ('LICENSES/InWorldRecipes-MIT.txt',),
 'matc': ('LICENSES/MysticalAgricultureTieredCrystals-MIT.txt',),
 'ae2wtlib': ('LICENSES/AE2WTLib-MIT.txt',),
 'measurements': ('LICENSES/Measurements-MIT.txt',)}
PACKAGES = {'collection': {'directory': 'resourcepack',
                'release': 'release.json',
                'notice': 'NOTICE.md',
                'filename': 'ATM11-Japanese-0.16.0.zip',
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
                               'extendedae',
                               'comforts',
                               'crafting_on_a_stick',
                               'toastcontrol',
                               'betteradvancedtooltips',
                               'toolbelt',
                               'cucumber',
                               'ironjetpacks',
                               'functionalstorage',
                               'buildinggadgets2',
                               'charginggadgets',
                               'curios',
                               'naturescompass',
                               'simplebackups',
                               'elevatorid',
                               'mysticalautomation',
                               'neoforge',
                               'moreoverlays',
                               'interdimensionalwirelesstransmitter',
                               'enchdesc',
                               'extremesoundmuffler',
                               'sfm',
                               'dimstorage',
                               'stepcrafter',
                               'refinedstorage_quartz_arsenal',
                               'keybindbundles',
                               'inworldrecipes',
                               'matc',
                               'ae2wtlib',
                               'measurements'),
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
                             'LICENSES/ExtendedAE-LGPL-3.0.txt',
                             'LICENSES/Comforts-LGPL-3.0-or-later.txt',
                             'LICENSES/Comforts-COPYING.txt',
                             'LICENSES/Comforts-COPYING.LESSER.txt',
                             'LICENSES/CraftingOnAStick-GPL-3.0.txt',
                             'LICENSES/ToastControl-MIT.txt',
                             'LICENSES/BetterAdvancedTooltips-MIT.txt',
                             'LICENSES/ToolBelt-BSD-3-Clause.txt',
                             'LICENSES/Cucumber-MIT.txt',
                             'LICENSES/IronJetpacks-MIT.txt',
                             'LICENSES/FunctionalStorage-MIT.txt',
                             'LICENSES/BuildingGadgets2-MIT.txt',
                             'LICENSES/ChargingGadgets-MIT.txt',
                             'LICENSES/Curios-LGPL-3.0-or-later.txt',
                             'LICENSES/Curios-COPYING.txt',
                             'LICENSES/Curios-COPYING.LESSER.txt',
                             'LICENSES/NaturesCompass-CC-BY-NC-SA-4.0.md',
                             'LICENSES/SimpleBackups-Apache-2.0.txt',
                             'LICENSES/ElevatorID-MIT.txt',
                             'LICENSES/MysticalAutomation-MIT.txt',
                             'LICENSES/NeoForge-LGPL-2.1.txt',
                             'LICENSES/MoreOverlays-MIT.txt',
                             'LICENSES/InterdimensionalWirelessTransmitter-MIT.txt',
                             'LICENSES/EnchantmentDescriptions-LGPL-2.1.txt',
                             'LICENSES/ExtremeSoundMuffler-LGPL-3.0.txt',
                             'LICENSES/SuperFactoryManager-MPL-2.0.txt',
                             'LICENSES/DimStorage-AGPL-3.0.txt',
                             'LICENSES/StepCrafter-MIT.txt',
                             'LICENSES/RefinedStorageQuartzArsenal-MIT.md',
                             'LICENSES/KeyBindBundles-MIT.txt',
                             'LICENSES/InWorldRecipes-MIT.txt',
                             'LICENSES/MysticalAgricultureTieredCrystals-MIT.txt',
                             'LICENSES/AE2WTLib-MIT.txt',
                             'LICENSES/Measurements-MIT.txt'),
                'pack': {'pack': {'description': 'ATM11 日本語改善 0.16.0: 52 namespaces / 3604 entries',
                                  'min_format': [84, 0],
                                  'max_format': [84, 0]},
                         'filter': {'block': [{'namespace': '^transmog$', 'path': '^lang/ja_jp\\.json$'}]}}}}
JEI_METADATA_VALUE = 'Debug (for a debug mode, do not need translation)'
# The whole original JAR is pinned above. This is the original JA runtime setting,
# not the English metadata or prose. No source JAR is needed to rebuild this pack.
JADE_ORIGINAL_JA_SHA256 = '381f227a22a7eb5cbf69c864752bd4fe72ea00f77ceed54df6b57b48550ba6b7'
JADE_METADATA_VALUE_SHA256 = 'e3cf5492749f2d1c3f333017f1aa6094138d2b02cd308c41432e25e2c51ad89a'


MULTISOURCE_KEY_SETS = {'ironjetpacks': {'lang': (41, '4b7816adcd5c0095ae9c4bd9ece59e54a00660e2ffec9ab89fc6cdc6553196b7'),
                  'materials': (14, 'b0760708c228ba12372bdb443ff216c737362b4ddfd1b19391a84e25e472caef')},
 'charginggadgets': {'lang': (6, 'a835f0e45a8f7adc97ad0a6467e7119ff78df0f419e777ec38a871340ac70aed'),
                     'configuration': (4,
                                       'b60ea67d7f9865875bd666c410997e46545d61a68cff2147966b83288b7e923f')},
 'keybindbundles': {'lang': (26, '62860b61aa47d370387753108c398e9216dca7f93c758c86504d6b6e632ec297'),
                    'configuration': (3, '6b47107a7220137579a20a4a61ffad7835f1749a2d033b332b1ad7e8d81561a2')}}
MULTISOURCE_BATCHES = {'lang-IronJetpacks-26.1.2-9.0.3-ironjetpacks-99d5e6d83d-0001': 'lang',
 'derived-ironjetpacks-materials-0001': 'materials',
 'lang-charginggadgets-1.16.1-charginggadgets-74380f08f3-0001': 'lang',
 'derived-charginggadgets-config-0001': 'configuration',
 'lang-keybindbundles-2.0.0-keybindbundles-648c3aa5a9-0001': 'lang',
 'derived-keybindbundles-config-0001': 'configuration'}


SFM_BATCH_IDS = ('lang-Super Factory Manager (SFM)-MC26.1.2-4.34.0-sfm-c0005bc889-0001',
 'lang-Super Factory Manager (SFM)-MC26.1.2-4.34.0-sfm-c0005bc889-0002',
 'lang-Super Factory Manager (SFM)-MC26.1.2-4.34.0-sfm-c0005bc889-0003',
 'lang-Super Factory Manager (SFM)-MC26.1.2-4.34.0-sfm-c0005bc889-0004',
 'lang-Super Factory Manager (SFM)-MC26.1.2-4.34.0-sfm-c0005bc889-0005')
ENCHDESC_METADATA_VALUES = {'__comment_jei': 'JEI Compat',
 '__support_betterarcheology': 'https://www.curseforge.com/minecraft/mc-mods/better-archeology',
 '__support_create_stuff': 'https://www.curseforge.com/minecraft/mc-mods/create-stuff-additions',
 '__support_deeperdarker': 'https://www.curseforge.com/minecraft/mc-mods/deeperdarker',
 '__support_dungeonsenchantments': 'https://www.curseforge.com/minecraft/mc-mods/dungeons-enchantments',
 '__support_endlessbiomes': 'https://www.curseforge.com/minecraft/mc-mods/endless-biomes',
 '__support_gofish': 'Go Fish support https://www.curseforge.com/minecraft/mc-mods/go-fish',
 '__support_grapplemod': 'Grapple Mod https://www.curseforge.com/minecraft/mc-mods/grappling-hook-mod',
 '__support_hunterillager': 'https://www.curseforge.com/minecraft/mc-mods/huntersreturn',
 '__support_improved_exp': 'https://www.curseforge.com/minecraft/mc-mods/improved-exp',
 '__support_shield+': 'Shields+ https://www.curseforge.com/minecraft/mc-mods/shieldsplus',
 '__support_stalwart_dungeons': 'https://www.curseforge.com/minecraft/mc-mods/stalwart-dungeons',
 '_comment': 'Vanilla Enchantment Descriptions'}

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
    policy = POLICIES[namespace]
    multisource = 'sources' in policy
    project_notice = PROJECT_NOTICES.get(namespace)
    evidence_fields = {'schema_version', 'namespace', 'language_sha256', 'reviews'}
    if project_notice is not None:
        evidence_fields.update({'source', 'project_notices'})
    evidence_fields.update({'version', 'sources'} if multisource else {'source'})
    schema = 4 if project_notice is not None else (3 if multisource else (2 if 'archive_chain' in policy else 1))
    require(isinstance(evidence, dict) and set(evidence) == evidence_fields and
            type(evidence['schema_version']) is int and evidence['schema_version'] == schema,
            f'{namespace}: Unexpected review evidence schema')
    require(evidence['namespace'] == namespace, f'{namespace}: Review namespace mismatch')
    if multisource:
        require(evidence['version'] == policy['version'] and evidence['sources'] == policy['sources'],
                f'{namespace}: Normal/derived source identity or English contract changed')
    else:
        require(evidence['source'] == policy, f'{namespace}: Review source/version/hash does not match the pinned MOD')
        validate_nested_identity(namespace, evidence['source'])
    if project_notice is not None:
        require(evidence['project_notices'] == project_notice,
                f'{namespace}: Project notice differs from the fixed Apache-4(b) notice')
        require(all(language.get(key) == value for key, value in project_notice.items()),
                f'{namespace}: Project notice language metadata must match the fixed notice')
    require(evidence['language_sha256'] == language_sha256, f'{namespace}: Review evidence language hash mismatch')
    reviews = evidence['reviews']
    require(isinstance(reviews, list) and bool(reviews), f'{namespace}: No independent review evidence')
    accepted, seen_reviews, seen_batches = set(), set(), set()
    accepted_by_source = {sid: set() for sid in policy['sources']} if multisource else {}
    for review in reviews:
        fields = {'batch_id', 'review_sha256', 'submission_sha256', 'reviewer', 'decision', 'accepted_keys'}
        if multisource:
            fields.add('source_id')
        require(isinstance(review, dict) and set(review) == fields, f'{namespace}: Unexpected review record schema')
        batch = review['batch_id']
        require(isinstance(batch, str) and (batch in SFM_BATCH_IDS if namespace == 'sfm' else re.fullmatch('[A-Za-z0-9_.+-]+', batch)) and batch not in seen_batches,
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
        if multisource:
            sid = review['source_id']
            require(isinstance(sid, str) and sid in accepted_by_source and MULTISOURCE_BATCHES.get(batch) == sid,
                    f'{namespace}: Review batch is bound to the wrong source')
            accepted_by_source[sid].update(keys)
        accepted.update(keys)
    if project_notice is not None:
        require(accepted == (set(language) - set(project_notice)),
                f'{namespace}: Source review keys must exclude the project notice metadata key')
    else:
        require(accepted == set(language), f'{namespace}: Language keys must exactly match the independently accepted key union')
    for sid, keys in accepted_by_source.items():
        count, key_hash = MULTISOURCE_KEY_SETS[namespace][sid]
        actual_hash = digest(json.dumps(sorted(keys), ensure_ascii=False, separators=(',', ':')).encode())
        require(len(keys) == count and actual_hash == key_hash,
                f'{namespace}/{sid}: Accepted keys differ from this source contract')



def validated_files(root, package='collection'):
    config = PACKAGES[package]
    release_raw = read_file(root, config['release'])
    release = parse(release_raw)
    require(isinstance(release, dict) and set(release) == {'schema_version', 'version', 'review_status', 'languages'} and
            type(release['schema_version']) is int and release['schema_version'] == 3,
            'Unexpected release manifest schema')
    require(release['review_status'] == 'accepted', 'Independent language review is pending; no ZIP generated')
    require(release['version'] == VERSION, 'This builder prepares version 0.16.0; earlier releases remain immutable')
    require(isinstance(release['languages'], dict) and set(release['languages']) == set(config['namespaces']),
            f'{package}: Only the fixed package namespaces are permitted')
    directory = config['directory']
    pack_raw = read_file(root, directory + '/pack.mcmeta')
    require(json.dumps(parse(pack_raw), sort_keys=True, ensure_ascii=False) ==
            json.dumps(config['pack'], sort_keys=True, ensure_ascii=False),
            f'{package}: Pack metadata/filter differs from the fixed policy')
    files = {'pack.mcmeta': pack_raw, 'release.json': release_raw,
             'README.md': read_file(root, 'README.md'), 'NOTICE.md': read_file(root, config['notice'])}
    require(digest(files['NOTICE.md']) == NOTICE_SHA256, 'Credits, modification notices or license scopes changed')
    allowed_pack_files = {'pack.mcmeta'}
    for namespace, record in release['languages'].items():
        expected_record_fields = {
            'language_sha256', 'key_count', 'preserved_metadata_keys', 'review_evidence_sha256',
        }
        if namespace in PROJECT_NOTICES:
            expected_record_fields.add('project_notice_keys')
        require(isinstance(record, dict) and set(record) == expected_record_fields,
                f'{namespace}: Unexpected language release record')
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
        if namespace in PROJECT_NOTICES:
            require(record['project_notice_keys'] == list(PROJECT_NOTICES[namespace]),
                    f'{namespace}: Project notice key declaration changed')
        if namespace == 'enchdesc':
            require(all(language.get(k) == v for k, v in ENCHDESC_METADATA_VALUES.items()),
                    'Enchantment Descriptions original metadata must remain verbatim')
        if namespace == 'jei':
            require(language['_comment'] == JEI_METADATA_VALUE, 'JEI metadata must remain verbatim')
        if namespace == 'measurements':
            require(language['_comment'] == 'NeoForge Config', 'Measurements metadata must remain verbatim')
        if namespace == 'naturescompass':
            require(language['_comment'] == 'STRINGS - PRECIPITATION', 'Nature’s Compass metadata must remain verbatim')
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
