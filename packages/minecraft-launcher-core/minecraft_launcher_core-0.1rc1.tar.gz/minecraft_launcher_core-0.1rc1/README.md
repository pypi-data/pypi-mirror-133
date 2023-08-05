#Minecraft launcher core
This is a minecraft launcher core
***
* Usage

       import launch
       test = launch.minecraft.Minecraft(<minecraft version path>)
       command = test.launch(
       
       size = list:[int:<width>,int:<height>],
       memorym = int:<min memory(MB)>
       memoryx = int:<max memory(MB)>
       username = string:<username in game>
       java = string:<java path>
       launcher = list:[string:<launcher name>,string:<laauncher version>]
       )
       print(commmand)
       '''
       this code can get minecraft start code.
       '''

       
       test = launch.find_version.Version(<.minecraft dir path>)
       names = test.get_list()
       print(names)
       '''
       this code can get minecraft versions in dir
       '''
       

