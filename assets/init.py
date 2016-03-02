#!/usr/bin/python
import json
import os
import re
import shutil
import sys
import time

__author__ = 'Sebastien LANGOUREAUX'

ALFRESCO_PATH = '/var/lib/ghost'

class ServiceRun():

  def set_database_connection(self, db_type, db_host, db_port, db_name, db_user, db_password):
      global ALFRESCO_PATH

      if db_type not in ["postgresql", "mysql"]:
          raise KeyError("DB type must be Postgresql or Mysql")

      if db_type == "mysql" and (db_host == "localhost" or db_host == "127.0.0.1"):
          raise KeyError("For local database, you must use Postgresql")

      if db_host != "localhost" and db_host != "127.0.0.1":
          self.replace_all('/etc/supervisor/conf.d/supervisord-postgresql.conf', 'autostart\s*=.*', 'autostart=false')
          self.replace_all('/etc/supervisor/conf.d/supervisord-postgresql.conf', 'autorestart\s*=.*', 'autorestart=false')
      else:
          self.replace_all('/etc/supervisor/conf.d/supervisord-postgresql.conf', 'autostart\s*=.*', 'autostart=true')
          self.replace_all('/etc/supervisor/conf.d/supervisord-postgresql.conf', 'autorestart\s*=.*', 'autorestart=true')

      if db_host is None or db_host == "":
          raise KeyError("You must provide db_host")

      if db_port is None or db_port == "":
          raise KeyError("You must provide db_port")

      if db_name is None or db_name == "":
          raise KeyError("You must provide db_name")

      if db_user is None or db_user == "":
          raise KeyError("You must provide db_user")

      if db_password is None or db_password == "":
          raise KeyError("You must provide db_password")

      db_conn_params = ""
      if db_type == "mysql":
          db_conn_params = "?useSSL=false"
          db_driver = "org.gjt.mm.mysql.Driver"
      else:
          db_driver = "org.postgresql.Driver"

      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'db.driver\s*=.*', 'db.driver=' + db_driver)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'db.username\s*=.*', 'db.username=' + db_user)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'db.password\s*=.*', 'db.password=' + db_password)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'db.name\s*=.*', 'db.name=' + db_name)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'db.url\s*=.*', 'db.url=jdbc:' + db_type + '://' + db_host + ':' + db_port + '/' + db_name + db_conn_params)


  def set_alfresco_context(self, host, port, protocol):
      global ALFRESCO_PATH

      if host is None or host == "":
          raise KeyError("You must provide host")

      if port is None or port == "":
          raise KeyError("You must provide port")

      if protocol is None or protocol == "":
          raise KeyError("You must provide protocol")

      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'alfresco.host\s*=.*', 'alfresco.host=' + host)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'alfresco.port\s*=.*', 'alfresco.port=' + port)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'alfresco.protocol\s*=.*', 'alfresco.protocol=' + protocol)

  def set_share_context(self, host, port, protocol):
      global ALFRESCO_PATH

      if host is None or host == "":
          raise KeyError("You must provide host")

      if port is None or port == "":
          raise KeyError("You must provide port")

      if protocol is None or protocol == "":
          raise KeyError("You must provide protocol")

      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'share.host\s*=.*', 'alfresco.host=' + host)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'share.port\s*=.*', 'alfresco.port=' + port)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'share.protocol\s*=.*', 'alfresco.protocol=' + protocol)

  def set_ftp(self, enable, port):
      global ALFRESCO_PATH

      if port is None or port == "":
          raise KeyError("You must provide port")

      if enable not in ["true", "false"]:
          raise KeyError("Enable must be true or false")

      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'ftp.enabled\s*=.*', 'ftp.enabled=' + enable)
      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'ftp.port\s*=.*', 'ftp.port=' + port)

  def set_core(self, environment):
      global ALFRESCO_PATH

      if environment not in ["UNKNOWN", "TEST", "BACKUP", "PRODUCTION"]:
          raise KeyError("Environment must be UNKNOWN, TEST, BACKUP or PRODUCTION")

      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'system.serverMode\s*=.*', 'system.serverMode=' + environment)


  def set_mail(self, host, port, user, password, protocol, starttls_enable, mail_sender):
      global ALFRESCO_PATH

      if host is not None and host != "":
          if port is None or port == "":
              raise KeyError("You must provide port")
          if protocol is None or protocol == "":
              raise KeyError("You must provide protocol")
          if mail_sender is None or mail_sender =="":
              raise KeyError("You must provide the mail sender")
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.host\s*=.*', 'mail.host=' + host)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.port\s*=.*', 'mail.port=' + port)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.protocol\s*=.*', 'mail.protocol=' + protocol)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.from.default\s*=.*', 'mail.from.default=' + mail_sender)
      else:
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.host\s*=', '#mail.host=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.port\s*=', '#mail.port=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.protocol\s*=', '#mail.protocol=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.from.default\s*=', 'mail.from.default=')

      if user is not None and user != "":
          if password is None or password == "":
              raise KeyError("You must provide password")
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.username\s*=.*', 'mail.username=' + username)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.password\s*=.*', 'mail.password=' + password)

          if protocol == "smtp":
              self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtp.auth\s*=.*', 'mail.smtp.auth=true')
              if starttls_enable == "true":
                  self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtp.starttls.enable\s*=.*', 'mail.smtp.starttls.enable=true')
              else:
                  self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtp.starttls.enable\s*=', '#mail.smtp.starttls.enable=')
          elif protocol == "smtps":
              self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtps.auth\s*=.*', 'mail.smtps.auth=true')
              if starttls_enable == "true":
                  self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtps.starttls.enable\s*=.*', 'mail.smtps.starttls.enable=true')
              else:
                  self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtps.starttls.enable\s*=', '#mail.smtps.starttls.enable=')
      else:
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.username\s*=', '#mail.username=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.password\s*=', '#mail.password=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtp.auth\s*=', '#mail.smtp.auth=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtps.auth\s*=', '#mail.smtps.auth=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtp.starttls.enable\s*=', '#mail.smtp.starttls.enable=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'mail.smtps.starttls.enable\s*=', '#mail.smtps.starttls.enable=')



  def set_cifs(self, enable, server_name, domain):
      global ALFRESCO_PATH

      if enable == "true":
          if server_name is None or server_name == "":
              raise KeyError("You must provide the server name")
          if domain is None or domain == "":
              raise KeyError("You must provide the domain")

          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.enabled\s*=.*', 'cifs.enabled=true')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.Server.Name\s*=.*', 'cifs.Server.Name=' + server_name)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.domain\s*=.*', 'cifs.domain=' + domain)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.hostannounce\s*=.*', 'cifs.hostannounce=true')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.broadcast\s*=.*', 'cifs.broadcast=0.0.0.255')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.ipv6.enabled\s*=.*', 'cifs.ipv6.enabled=false')
      else:
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.enabled\s*=', '#cifs.enabled=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.Server.Name\s*=', '#cifs.Server.Name=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.domain\s*=', '#cifs.domain=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.hostannounce\s*=', '#cifs.hostannounce=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.broadcast\s*=', '#cifs.broadcast=')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'cifs.ipv6.enabled\s*=', '#cifs.ipv6.enabled=')

  def set_ldap(self, enable, auth_format, host, user, password, list_admins, search_base_group, search_base_user):
      global ALFRESCO_PATH

      if enable == "true":
          if auth_format is None or auth_format == "":
              raise KeyError("You must provide auth_format")
          if host is None or host == "":
              raise KeyError("You must provide host")
          if user is None or user == "":
              raise KeyError("You must provide user")
          if password is None or password == "":
              raise KeyError("You must provide password")
          if list_admins is None or list_admins == "":
              raise KeyError("You must provide list admins")
          if search_base_group is None or search_base_group == "":
              raise KeyError("You must provide the search base group")
          if search_base_user is None or search_base_user == "":
              raise KeyError("You must provide the search base user")

          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'authentication.chain\s*=.*', 'authentication.chain=alfrescoNtlm1:alfrescoNtlm,ldap1:ldap')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.propertie', 'ldap.authentication.userNameFormat\s*=.*', 'ldap.authentication.userNameFormat=' + auth_format)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.propertie', 'ldap.authentication.java.naming.provider.url\s*=.*', 'ldap.authentication.java.naming.provider.url=ldap://' + host + ':389')
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.propertie', 'ldap.authentication.defaultAdministratorUserNames\s*=.*', 'ldap.authentication.defaultAdministratorUserNames=' + list_admins)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.propertie', 'ldap.synchronization.java.naming.security.principal\s*=.*', 'ldap.synchronization.java.naming.security.principal=' + user)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.propertie', 'ldap.synchronization.java.naming.security.credentials\s*=.*', 'ldap.synchronization.java.naming.security.credentials=' + password)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.propertie', 'ldap.synchronization.groupSearchBase\s*=.*', 'ldap.synchronization.groupSearchBase=' + search_base_group)
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.propertie', 'ldap.synchronization.userSearchBase\s*=.*', 'ldap.synchronization.userSearchBase=' + search_base_user)
      else:
          self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'authentication.chain\s*=.*', 'authentication.chain=alfrescoNtlm1:alfrescoNtlm')

  def replace_all(self, file, searchRegex, replaceExp):
    """ Replace String in file with regex
    :param file: The file name where you should to modify the string
    :param searchRegex: The pattern witch must match to replace the string
    :param replaceExp: The string replacement
    :return:
    """

    regex = re.compile(searchRegex, re.IGNORECASE)

    f = open(file,'r')
    out = f.readlines()
    f.close()

    f = open(file,'w')

    for line in out:
      if regex.search(line) is not None:
        line = regex.sub(replaceExp, line)

      f.write(line)

    f.close()


  def add_end_file(self, file, line):
    """ Add line at the end of file
    :param file: The file where you should to add line to the end
    :param line: The line to add in file
    :return:
    """
    with open(file, "a") as myFile:
        myFile.write("\n" + line + "\n")






if __name__ == '__main__':

    serviceRun = ServiceRun()

    # We set database
    serviceRun.set_database_connection(os.getenv('DATABASE_TYPE', 'postgresql'), os.getenv('DATABASE_HOST', 'localhost'), os.getenv('DATABASE_PORT', '5432'), os.getenv('DATABASE_NAME', 'alfresco'), os.getenv('DATABASE_USER', 'alfresco'), os.getenv('DATABASE_PASSWORD', 'admin'))

    # We set alfresco url
    serviceRun.set_alfresco_context(os.getenv('ALFRESCO_HOSTNAME', '127.0.0.1'), os.getenv('ALFRESCO_PORT', '8080'), os.getenv('ALFRESCO_PROTOCOL', 'http'))

    # We set share url
    serviceRun.set_share_context(os.getenv('SHARE_HOSTNAME', '127.0.0.1'), os.getenv('SHARE_PORT', '8080'), os.getenv('SHARE_PROTOCOL', 'http'))

    # We set ftp
    serviceRun.set_ftp(os.getenv('FTP_ENABLED', 'true'), os.getenv('FTP_PORT', '21'))

    # We set environment
    serviceRun.set_core(os.getenv('ENVIRONMENT', 'PRODUCTION'))

    # We set mail
    serviceRun.set_mail(os.getenv('MAIL_HOST', 'localhost'), os.getenv('MAIL_PORT', '25'), os.getenv('MAIL_USER'), os.getenv('MAIL_PASSWORD'), os.getenv('MAIL_PROTOCOL', 'smtp'), os.getenv('MAIL_STARTTLS_ENABLE', 'false'), os.getenv('MAIL_SENDER', 'alfresco@alfresco.org'))

    # We set CIFS
    serviceRun.set_cifs(os.getenv('CIFS_ENABLED', 'true'), os.getenv('CIFS_SERVER_NAME', 'localhost'), os.getenv('CIFS_DOMAIN', 'WORKGROUP'))

    # We set LDAP
    serviceRun.set_ldap(os.getenv('LDAP_ENABLED', 'false'), os.getenv('LDAP_AUTH_FORMAT'), os.getenv('LDAP_HOST'), os.getenv('LDAP_USER'), os.getenv('LDAP_PASSWORD'), os.getenv('LDAP_ADMINS'), os.getenv('LDAP_GROUP_SEARCHBASE'), os.getenv('LDAP_USER_SEARCHBASE'))
