#!/usr/bin/python
#coding:utf-8

import os
from os.path import dirname,abspath
import sys
import time

class tool():

    #获取本项目的根目录
    @staticmethod
    def read( file, mode="r+"):
        lines = [];
        fh = open(file, mode)
        try:
            for line in fh.readlines():
                if line.rstrip() == "":continue;
                lines.append(line.rstrip());
        finally:
            fh.close();
        return lines;

    @staticmethod
    def write(file, content, mode='w'):
        fh = open(file, mode)
        try:
            fh.write(content)
        finally:
            fh.close();
        return;



    #读取这个服的配置
    @staticmethod
    def getCoinfg( Serverfile ):
        arrConfig = {}
        #读取配这个服的配置
        #Serverfile = dirname( abspath( __file__ ) )+"/param.txt"               #修改服务器的脚本存放点
        fp = open( Serverfile, "r+"  )
        msg = fp.readlines()
        for index in msg:
            index = index.replace( "\n","" )
            
            i = 0
            pix = 0
            while i < len( index ):
                if( index[i] == "=" ):
                    pix = i
                    break
                i=i+1
            arrConfig[ index[0:i] ] = index[(i+1):len(index)]
        
        fp.close()
        return arrConfig
        pass

    #读取这个服的配置
    @staticmethod
    def getHostPort( Domain ):
        arrConfig = {}
        s_Domain = Domain.replace( "http://", "" )
        s_Domain = Domain.replace( "https://", "" )
        Return = []

        HostPort = s_Domain.split(":")

        Return.append( str(HostPort[0]) )#域名
        if(len(HostPort)< 2):    #端口
            Return.append( "80" )#端口
        else:
            Return.append( str(HostPort[1]) )#端口
        return Return
        pass




class script( ):

    __ServerInfo = {}
    __APP_Path   = ""           #程序的根目录
    def __init__( self ):
        Serverfile = dirname( abspath( __file__ ) )+"/param.txt"               #修改服务器的脚本存放点
        self.__ServerInfo = tool().getCoinfg( Serverfile )

        self.__APP_Path = dirname(dirname( abspath( __file__ ) ))
        pass



    def serverConfig( self ):    #完成

        Language='zh_chs'
        TimeZone='Asia/Shanghai'
        # if ( self.__ServerInfo['APP.Language']==3 or self.__ServerInfo['APP.Language']=='3' ):
        #     Language='Traditional'
        #     pass
        if (self.__ServerInfo['APP.LanguageCode']!=''):
            Language=self.__ServerInfo['APP.LanguageCode']
            pass
        if (self.__ServerInfo['APP.TimeZone']!=''):
            TimeZone=self.__ServerInfo['APP.TimeZone']
            pass

        Db_ConnectIP = self.__ServerInfo['APP.DbIp']
        if( self.__ServerInfo['APP.TargetIp'] == self.__ServerInfo['APP.DbIp'] ):
            Db_ConnectIP = "127.0.0.1"
            pass
            
        Configs = """<?php
#不能增加应和的配置 
return array(

    'Charset'   =>  'UTF-8',                //本服编码
    'Language'  =>  '"""+Language+"""',     //语言包为简单中文
    'TimeZone'  =>  '"""+TimeZone+"""',     //程序时区

    'LogType'  =>  '1',                     //使用日志平台开关(1:使用 0:不使用)
    
    //数据库配置 BEGIN
    'Database' => array(//数据库连接(主库)
        'host'      => '"""+Db_ConnectIP+"""',
        'user'      => '"""+self.__ServerInfo['APP.DbUser']+"""',
        'password'  => '"""+self.__ServerInfo['APP.DbPassword']+"""',
        'database'  => '"""+self.__ServerInfo['APP.DbName']+"""',
        'charset'   => 'utf8mb4',
        'prefix'    => 'tb_',//tb_
    ),

    /*
    'RDatabase' => array(//数据库连接(从库,如果需要只用来select处理的)(可以不存在)
        'host'      => '127.0.0.1',
        'user'      => 'root',
        'password'  => 'root',
        'database'  => '"""+Db_ConnectIP+"""',
        'charset'   => 'utf8',
    ),
    */

    //数据库配置 记录大数据配置
    'BigLog' => array(//记录通信量大数量    
        'opera' => 0,       //记录大数据的开关
        'size' => 1000, //记录大数据的长度
    ),
    

    //memcache存储配置
    'MemCache' => array(//Memcache
        'host' => '127.0.0.1',
        'port' => '11211',
        'dbname' => '"""+self.__ServerInfo['APP.DbName']+"""',
    ),

    //redis存储配置
    'Redis' => array(//Memcache
        'host' => '192.168.1.124',
        'port' => '6379',
        'DBID' => '1',
    ),
    

    //socket存储配置
    'Socket' => array(//socket
        'host'  => '127.0.0.1',         //python服务器的地址
        'ip'    => '127.0.0.1',         //python服务器的地址(最好是内网IP)
        'port'  => '3195' ,             //服务器与服务器之间通信端口
        'passkey'=> 'password',         //通信之间的加密串
    ),

    //最后更新的信息
    'Update_info' => array(
        'LastTime' =>'"""+time.strftime("%Y-%m-%d %H:%M:%S")+"""',   //最后一次更新的时间  
        'Version' =>'"""+self.__ServerInfo['Queue.VersionName']+"""', //当前的版本
    ),

);
""";
        #Configs = unicode("".Configs, 'utf8');
        ServerCfg = self.__APP_Path+"/server/core/config.php"
        shells = ":> %s"%( ServerCfg )
        os.system( shells )
        fp = open( ServerCfg, "r+"  )
        fp.write( Configs )
        fp.close()
        print ServerCfg

        Configs = """<?php
#不能增加应和的配置 
return array(
    'MainPeer'  => array(
        'ServerId'      =>  """+self.__ServerInfo['Main.ApplicationId']+""",//应用的唯一ID     
        'ServerName'    =>  '"""+self.__ServerInfo['Main.AppName']+"""',    //应用名称
        'ServerType'    =>  """+self.__ServerInfo['Main.ClassType']+""",    //服务类型 1聊天 2匹配 3战斗 4分服 5平台 6通讯站 7日志 8配置
        'ServerRoom'    =>  """+self.__ServerInfo['Main.ServerRoom']+""",   //机房ID
        'Net'           =>  """+self.__ServerInfo['Main.Net']+""",          //1http 2https 3socket 4websocket 5websocketssl
        'VipHost'       => '"""+self.__ServerInfo['Main.Slot1']+"""',       //VIP代理访问(供客户端使用)
        'Host'          => '"""+self.__ServerInfo['Main.Host']+"""',        //应用的访问外网地址IP:端口
        'InnerHost'     => '"""+self.__ServerInfo['Main.InnerHost']+"""',   //应用的访问内网地址IP:端口
        'PassKey'       => '"""+self.__ServerInfo['Main.PassKey']+"""',     //应用之间通信的密钥
        'State'          => 1,          //应用的状态
        'StartTime'     => """+self.__ServerInfo['Main.CreateTime']+""",    //应用的开服时间
        
    ),
    
    'Server'    => array(
            'ServerId'      =>  """+self.__ServerInfo['APP.ApplicationId']+""",   //应用的唯一ID             
            'ServerName'    =>  '"""+self.__ServerInfo['APP.AppName']+"""',       //应用名称
            'ServerType'    =>  """+self.__ServerInfo['APP.ClassType']+""",       //服务类型 1聊天 2匹配 3战斗 4分服 5平台 6通讯站 7日志 8配置
            'ServerRoom'    =>  """+self.__ServerInfo['APP.ServerRoom']+""",      //机房ID
            'Net'           =>  """+self.__ServerInfo['APP.Net']+""",             //1http 2https 3socket 4websocket 5websocketssl
            'VipHost'       =>  '"""+self.__ServerInfo['APP.Slot1']+"""',       //VIP代理访问(供客户端使用)
            'Host'          =>  '"""+self.__ServerInfo['APP.Host']+"""',          //应用的访问外网地址IP:端口
            'InnerHost'     =>  '"""+self.__ServerInfo['APP.InnerHost']+"""',     //应用的访问内网地址IP:端口
            'PassKey'       =>  '"""+self.__ServerInfo['APP.PassKey']+"""',       //应用之间通信的密钥
            'UserPassKey'   =>  '"""+self.__ServerInfo['APP.UserPassKey']+"""',   //应用的开服时间
            'State'         =>  1, //应用的状态
            'StartTime'     =>  """+self.__ServerInfo['APP.CreateTime']+""",  //应用的开服时间
            'Ip'            =>  '"""+self.__ServerInfo['APP.TargetIp']+"""',        //ip
            'Port'          =>  """+self.__ServerInfo['APP.Port']+""",        //端口
            'InnerIp'       =>  '"""+self.__ServerInfo['APP.TargetInnerIp']+"""',   //内网ip
            'InnerPort'     =>  """+self.__ServerInfo['APP.InnerPort']+""",   //内网端口
            'ServerDir'     =>  '"""+self.__ServerInfo['APP.SrcDir']+"""',    //服务路劲
            'SSHPort'       =>  """+self.__ServerInfo['APP.TargetPort']+""",  //ssh端口
            'Rand'          =>  100,                                          //随机机率
            'Group'         =>  6666666,                                      //默认测试分组
        ),
);
?>
""";
        #Configs = unicode("".Configs, 'utf8');
        ServerCfg = self.__APP_Path+"/server/gamecore/game_config.php"
        shells = ":> %s"%( ServerCfg )
        os.system( shells )
        fp = open( ServerCfg, "r+"  )
        fp.write( Configs )
        fp.close()
        print ServerCfg

        cmd = "find %s -type d -name '.svn'|xargs rm -Rf"%( self.__APP_Path )
        os.system( cmd )
        cmd = "find %s -type d -name '.svn-base'|xargs rm -Rf"%( self.__APP_Path )
        os.system( cmd )
        pass




    def nginx(self, Access = 0, conf='/usr/server/nginx0.7/conf/nginx.conf', backup=True ):
        if backup:
            shell = "cp %s %s.bak"%( conf, conf )
            os.system( shell )

        NginxLines = tool().read(conf);
        NginxConfig = unicode("".join(NginxLines), 'utf8');
        addNginxConfig = "" #最后加入到nginx配置中

        #要加跨域处理
        #Access = 1

        HostPort = tool().getHostPort( self.__ServerInfo['APP.Host'] )
        WebHost  = str(HostPort[0])
        WebPort  = str(HostPort[1])
        #如果外部端口不是指向80
        if WebPort != "80":
            PortDomainsDir = "  root [DomainsDir];"
            PortDomainsDir = PortDomainsDir.replace( "[DomainsDir]", self.__APP_Path )
            PortListen = "  listen [Port];"
            PortListen = PortListen.replace( "[Port]", WebPort )

            PortTemplate = []
            PortTemplate.append( "server {" )
            PortTemplate.append( PortListen )
            PortTemplate.append( "  access_log off;" )
            PortTemplate.append( "  error_log /dev/null crit;" )
            PortTemplate.append( "  index index.html index.php index.htm;" )
            PortTemplate.append( PortDomainsDir )#
            if Access == 1:
                PortTemplate.append( "  add_header Access-Control-Allow-Origin *;" )
                PortTemplate.append( "  add_header Access-Control-Allow-Methods 'GET, POST';" )
                pass
            PortTemplate.append( "  location ~ ^/(server/log|server/expand|server/crons/config|server/crons/install|server/crons/crontab) {deny all;include fastcgi_params;}" )#
            PortTemplate.append( "  location ~ .*\.(php|php5)?$ {" )
            PortTemplate.append( "     include fastcgi_params;" )
            PortTemplate.append( "  }" )
            PortTemplate.append( "  if (-d $request_filename) {" )
            PortTemplate.append( "       rewrite ^/(.*)([^/])$ http://$host/$1$2/ permanent;" )
            PortTemplate.append( "  }" )
            PortTemplate.append( "  location ~* ^.+\.(sql|tar|gz|tar.gz)$ {" )
            PortTemplate.append( "       return 404;" )
            PortTemplate.append( "  }" )
            PortTemplate.append( "  location ~* ^.+\.(gif|jpg|png|js)$ {" )
            PortTemplate.append( "   expires      30m;" )
            PortTemplate.append( "  }" )
            PortTemplate.append( "}" )
            PortTemplate_u = unicode("".join(PortTemplate), 'utf8');
            if PortTemplate_u not in NginxConfig: #如果在里面，在下面替换了
                addNginxConfig = addNginxConfig + ("\n".join(PortTemplate))
                pass
            pass
        #

        #print addNginxConfig
        #exit(1)

        #================================主要修改addNginxConfig START=======================================#
        #
        #默认的nginx配置BEGIN
        Domains = "  server_name [Domains];"
        DomainsDir = "  root [DomainsDir];"

        Domains = Domains.replace( "[Domains]", WebHost )
        DomainsDir = DomainsDir.replace( "[DomainsDir]", self.__APP_Path )

        httpsCfg = [
            "xyou.cn",
            "bizgame.com",
            "bcpgame.com",
            "heroschool.info"
        ]
        httpsDomain = ""
        for x in httpsCfg:
            if x in Domains:
                httpsDomain = x
                break
        HttpTemplate = []
        HttpTemplate.append( "server {" )
        HttpTemplate.append( "  listen 80;" )

        if httpsDomain != "":#存在https，需要使用证书
            HttpTemplate.append( "  listen 443;" )
            HttpTemplate.append( Domains )
            HttpTemplate.append( "  ssl on;" )
            HttpTemplate.append( "  ssl_certificate /usr/server/nginx0.7/conf/"+httpsDomain+".crt;" )
            HttpTemplate.append( "  ssl_certificate_key /usr/server/nginx0.7/conf/"+httpsDomain+".key;" )
            pass
        else:#只需要http,不需要https证书
            HttpTemplate.append( Domains )
            pass
        HttpTemplate.append( "  access_log off;" )
        HttpTemplate.append( "  error_log /dev/null crit;" )
        HttpTemplate.append( "  index index.html index.php index.htm;" )
        HttpTemplate.append( DomainsDir )#
        if Access == 1:
           HttpTemplate.append( "  add_header Access-Control-Allow-Origin *;" )
           HttpTemplate.append( "  add_header Access-Control-Allow-Methods 'GET, POST';" )
           pass
        HttpTemplate.append( "  location ~ ^/(server/crons/python|server/crons/install|plugins/amfphp/browser) {deny all;include fastcgi_params;}" )#
        HttpTemplate.append( "  location ~ .*\.(php|php5)?$ {" )
        HttpTemplate.append( "     include fastcgi_params;" )
        HttpTemplate.append( "  }" )
        HttpTemplate.append( "  if (-d $request_filename) {" )
        HttpTemplate.append( "       rewrite ^/(.*)([^/])$ http://$host/$1$2/ permanent;" )
        HttpTemplate.append( "  }" )
        HttpTemplate.append( "  location ~* ^.+\.(sql|tar|gz|tar.gz)$ {" )
        HttpTemplate.append( "       return 404;" )
        HttpTemplate.append( "  }" )
        HttpTemplate.append( "  location ~* ^.+\.(gif|jpg|png|js)$ {" )
        HttpTemplate.append( "   expires      30m;" )
        HttpTemplate.append( "  }" )
        HttpTemplate.append( "}" )
        HttpTemplate_u = unicode("".join(HttpTemplate), 'utf8');

        if HttpTemplate_u not in NginxConfig: #如果在里面，在下面替换了
            if addNginxConfig != "":
                addNginxConfig = addNginxConfig +"\n"
                pass
            addNginxConfig = addNginxConfig +("\n".join(HttpTemplate))
            pass
        #默认的nginx配置END

        

        #内网nginx配置BEGIN
        InnerHostPort = tool().getHostPort( self.__ServerInfo['APP.InnerHost'] )
        InnerWebHost  = str(InnerHostPort[0])
        InnerWebPort  = str(InnerHostPort[1])
        if InnerWebPort != "80":
            innerTemplate = []
            innerTemplate.append( "server {" )
            innerTemplate.append( "  listen "+InnerWebPort+";" )
            innerTemplate.append( "  server_name localhost;" )#
            innerTemplate.append( "  access_log off;" )
            innerTemplate.append( "  error_log /dev/null crit;" )
            innerTemplate.append( "  index index.html index.php index.htm;" )
            innerTemplate.append( DomainsDir )#
            innerTemplate.append( "  location ~ ^/(server/crons/python|server/crons/install|plugins/amfphp/browser) {deny all;include fastcgi_params;}" )#
            innerTemplate.append( "  location ~ .*\.(php|php5)?$ {" )
            innerTemplate.append( "     include fastcgi_params;" )
            innerTemplate.append( "  }" )
            innerTemplate.append( "  if (-d $request_filename) {" )
            innerTemplate.append( "       rewrite ^/(.*)([^/])$ http://$host/$1$2/ permanent;" )
            innerTemplate.append( "  }" )
            innerTemplate.append( "  location ~* ^.+\.(sql|tar|gz|tar.gz)$ {" )
            innerTemplate.append( "       return 404;" )
            innerTemplate.append( "  }" )
            innerTemplate.append( "  location ~* ^.+\.(gif|jpg|png|js)$ {" )
            innerTemplate.append( "   expires      30m;" )
            innerTemplate.append( "  }" )
            innerTemplate.append( "}" )
            innerTemplate_u = unicode("".join(innerTemplate), 'utf8');
            if innerTemplate_u not in NginxConfig: #如果在里面，在下面替换了
                if addNginxConfig != "":
                    addNginxConfig = addNginxConfig +"\n"
                pass
                addNginxConfig = addNginxConfig +("\n".join(innerTemplate))
                pass
        #内网nginx配置END
        #
        #================================主要修改addNginxConfig END =======================================#
        #
        #nginx需要作修改
        if addNginxConfig != "":
            del NginxLines[len(NginxLines)-1];
            NginxLines.append( addNginxConfig )
            NginxLines.append("}");
            newFile = "\n".join(NginxLines)
            tool().write(conf, newFile);
            shell = "/etc/init.d/nginx reload"
            os.system( shell )
            pass
        return 1


    def crontab(self, conf='/var/spool/cron/root', backup=True):    #完成

        if backup:
            shell = "cp %s %s.bak"%( conf, conf )
            os.system( shell )
        lines = tool().read(conf);

        template = []

        sh_Tem = "*/1 * * * * [Path]/server/crons/crontab/auto_exe.sh [Dirname] > /dev/null 2>&1"
        sh_Tem = sh_Tem.replace( "[Path]", self.__APP_Path )
        sh_Tem = sh_Tem.replace( "[Dirname]", self.__ServerInfo['APP.SrcDir'] )
        template.append( sh_Tem )

        sh_Tem = "*/1 * * * * [Path]/server/crons/crontab/robot_exe.sh [Dirname] > /dev/null 2>&1"
        sh_Tem = sh_Tem.replace( "[Path]", self.__APP_Path )
        sh_Tem = sh_Tem.replace( "[Dirname]", self.__ServerInfo['APP.SrcDir'] )
        template.append( sh_Tem )

        for temp in template:
            if len(lines) == 0 or temp not in lines:
                lines.append("%s" % temp);
        lines.append("");
        tool().write(conf, "\n".join(lines)); 
        return 0;


    #初始化程序
    def InitGame( self ):
        ServerCfg = self.__APP_Path+"/server/crons/install/running.php 1"
        shells = "php -f %s"%( ServerCfg )
        print shells
        os.system( shells )
        pass

    #更新程序
    def UpdateGame( self ):
        ServerCfg = self.__APP_Path+"/server/crons/update/running.php 1"
        shells = "php -f %s"%( ServerCfg )
        print shells
        os.system( shells )
        pass

    #删除初始化程序
    def DelInitGame( self ):
        ServerCfg = self.__APP_Path+"/server/crons/install/"
        shells = "rm -Rf %s"%( ServerCfg )
        print shells
        os.system( shells )
        pass


    #设权限
    def Permission(self ):
        Shells = "chown -Rf rhgame:rhgame [Dir]"
        Shells = Shells.replace( "[Dir]", self.__APP_Path )
        os.system( Shells )

        #配置
        sh_Tem = "chmod -Rf 0777 [PATH]/server/crons/config"
        sh_Tem = sh_Tem.replace( "[PATH]", self.__APP_Path )
        os.system( sh_Tem )

        #日志目录
        logDir="%s/server/log"%(self.__APP_Path)
        if os.path.exists(logDir) == False:
            shells = "mkdir %s"%(logDir)
            print shells
            os.system( shells )
        shells = "chmod -Rf 0777 %s"%(logDir)
        print shells
        os.system( shells )

        #log/db
        dbDir="%s/server/log/db"%(self.__APP_Path)
        if os.path.exists(dbDir) == False:
            shells = "mkdir %s"%(dbDir)
            print shells
            os.system( shells )
        shells = "chmod -Rf 0777 %s"%(dbDir)
        print shells
        os.system( shells )

        #log/online_log
        onlineDir="%s/server/log/online_log"%(self.__APP_Path)
        if os.path.exists(onlineDir) == False:
            shells = "mkdir %s"%(onlineDir)
            print shells
            os.system( shells )
        shells = "chmod -Rf 0777 %s"%(onlineDir)
        print shells
        os.system( shells )

        #log/BattleInvite
        binviteDir="%s/server/log/BattleInvite"%(self.__APP_Path)
        if os.path.exists(binviteDir) == False:
            shells = "mkdir %s"%(binviteDir)
            print shells
            os.system( shells )
        shells = "chmod -Rf 0777 %s"%(binviteDir)
        print shells
        os.system( shells )


        #下载配置
        downDir="%s/server/download"%(self.__APP_Path)
        if os.path.exists(downDir) == False:
            shells = "mkdir %s"%(downDir)
            print shells
            os.system( shells )
        shells = "chmod -Rf 0777 %s"%(downDir)
        print shells
        os.system( shells )

        #下载配置
        #sh_Tem = "chmod -Rf 0777 [PATH]/server/download"
        #sh_Tem = sh_Tem.replace( "[PATH]", self.__APP_Path )
        #print(sh_Tem)
        #os.system( sh_Tem )

        #ssh给可执行权限
        sh_Tem = "chmod -Rf +x [PATH]/server/crons/crontab/auto_exe.sh"
        sh_Tem = sh_Tem.replace( "[PATH]", self.__APP_Path )
        print(sh_Tem)
        os.system( sh_Tem )

        sh_Tem = "chmod -Rf +x [PATH]/server/crons/crontab/robot_exe.sh"
        sh_Tem = sh_Tem.replace( "[PATH]", self.__APP_Path )
        print(sh_Tem)
        os.system( sh_Tem )
        pass
    

    #更新程序配置文件
    def UpdateGameConfigFile( self ):
        ServerCfg = dirname( abspath( __file__ ) )+"/../server/crons/config/encrypt/encrypt.php"
        shells = "php -f %s"%( ServerCfg )
        print shells
        os.system( shells )
        pass

    #重启GameServer 和memcached
    def restartServer( self ):
        shells = "/root/bin/killmemcached"
        print shells
        os.system( shells )
        pass


    #启动C++服务端
    def StartCplus( self ):
         if self.__ServerInfo['Type'] == "1" or self.__ServerInfo['Type'] == 1:      #只针对分服有作用
            CpulsShell = dirname( abspath( __file__ ) )+"/../server/crons/cplus/GameServer %s"%(self.__ServerInfo['SrcDir'])
            shells = "setsid  %s"%( CpulsShell )
            #os.system( shells ) #删除C++端服端的源代码
            pass



    def start( self ):
        #print self.__ServerInfo
        self.serverConfig()         #修改分服的config.php配置
        if int(self.__ServerInfo['APP.IsOpen']) == 1:  #开新服
            self.nginx( 1 )            #修改nginx.conf的配置
            self.crontab()          #修改crontab 的数据
            self.InitGame()         #初始化程序
            pass
        else:
            self.UpdateGame()
            self.DelInitGame()
            pass
        self.Permission()     #设置目录支持sftp上传修改
        self.UpdateGameConfigFile()
        self.restartServer()        #重启GameServer 和memcached
        pass

if  __name__ == '__main__':
    scri = script()
    scri.start()
    pass
