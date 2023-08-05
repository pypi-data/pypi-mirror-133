

import file,json

class server:
    def __init__(self,version):
        self.version = version
    def load(self):
        try:

            os.mkdir(r'C:\Users\Default\AppData\Roaming\.mcl')
        except BaseException as e:
            pass
        self.basepath = r'C:\Users\Default\AppData\Roaming\.mcl'
        file.File('https://launchermeta.mojang.com/mc/game/version_manifest.json',self.basepath+'\\versions.json')

        with open(self.basepath+'\\versions.json') as f:
            self.content = f.read()

        for i in eval(self.content)['versions']:
            if i['id'] == self.version:
                self.dic = i

                return
        raise SystemError(''
                          'This version does not exist.')
    def download_server_core_jar(self,dir):
        file.File(self.dic['url'], dir + '\\server.json')
        self.ser = json.load(open(dir + '\\server.json'))
        while True:

            try:

                file.File(self.ser['downloads']['server']['url'],dir+'\\server.jar')
                break
            except BaseException as e:
                continue
        with open(dir+'\\eula.txt','w') as f:
            f.write('eula=true')
    def setting_default(self):
        self.setting_add("D:\\server", 'allow-flight', 'false')
        self.setting_add("D:\\server", 'allow-nether', 'true')
        self.setting_add("D:\\server", 'broadcast-console-to-ops', 'true')
        self.setting_add("D:\\server", 'broadcast-rcon-to-ops', 'true')
        self.setting_add("D:\\server", 'difficulty', 'peaceful')
        self.setting_add("D:\\server", 'enable-command-block', 'false')
        self.setting_add("D:\\server", 'enable-jmx-monitoring', 'false')
        self.setting_add("D:\\server", 'enable-query', 'false')
        self.setting_add("D:\\server", 'enable-rcon', 'false')
        self.setting_add("D:\\server", 'enable-status', 'true')
        self.setting_add("D:\\server", 'enforce-whitelist', 'false')
        self.setting_add("D:\\server", 'entity-broadcast-range-percentage', '100')
        self.setting_add("D:\\server", 'force-gamemode', 'false')
        self.setting_add("D:\\server", 'function-permission-level', '2')
        self.setting_add("D:\\server", 'gamemode', 'survival')
        self.setting_add("D:\\server", 'generate-structures', 'true')
        self.setting_add("D:\\server", 'generator-settings', '')
        self.setting_add("D:\\server", 'hardcore', 'false')
        self.setting_add("D:\\server", 'hide-online-players', 'false')
        self.setting_add("D:\\server", 'level-name', 'world')
        self.setting_add("D:\\server", 'level-seed', '')
        self.setting_add("D:\\server", 'level-type', 'default')
        self.setting_add("D:\\server", 'max-build-height', '256')
        self.setting_add("D:\\server", 'max-players', '20')
        self.setting_add("D:\\server", 'max-tick-time', '60000')
        self.setting_add("D:\\server", 'max-world-size', '29999984')
        self.setting_add("D:\\server", 'motd', 'A minecraft server')
        self.setting_add("D:\\server", 'network-compression-threshold', '256')
        self.setting_add("D:\\server", 'online-mode', 'true')
        self.setting_add("D:\\server", 'op-permission-level', '4')
        self.setting_add("D:\\server", 'player-idle-timeout', '0')
        self.setting_add("D:\\server", 'prevent-proxy-connections', 'false')
        self.setting_add("D:\\server", 'pvp', 'true')
        self.setting_add("D:\\server", 'query.port', '25565')
        self.setting_add("D:\\server", 'rate-limit', '0')
        self.setting_add("D:\\server", 'rcon.password', '')
        self.setting_add("D:\\server", 'rcon.port', '25575')
        self.setting_add("D:\\server", 'require-resource-pack', 'false')
        self.setting_add("D:\\server", 'resource-pack', '')
        self.setting_add("D:\\server", 'resource-pack-prompt', '')
        self.setting_add("D:\\server", 'resource-pack-sha1', '')
        self.setting_add("D:\\server", 'server-ip', '')
        self.setting_add("D:\\server", 'server-port', '25565')
        self.setting_add("D:\\server", 'spawn-animals', 'true')
        self.setting_add("D:\\server", 'spawn-monsters', 'true')
        self.setting_add("D:\\server", 'spawn-npcs', 'true')
        self.setting_add("D:\\server", 'spawn-protection', '16')
        self.setting_add("D:\\server", 'sync-chunk-writes', 'true')
        self.setting_add("D:\\server", 'use-native-transport', 'true')
        self.setting_add("D:\\server", 'view-distance', '10')
        self.setting_add("D:\\server", 'white-list', 'false')

    def setting_add(self,dir,a,b):
        with open(dir+'\\server.properties','a') as f:
            f.write(f'{a}={b}')
if __name__ == '__main__':
    a = server('1.16.5')
    # a.load()
    # a.download_server_core_jar("D:\\server")





