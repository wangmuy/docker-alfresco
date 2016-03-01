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

      self.replace_all(ALFRESCO_PATH + '/tomcat/shared/classes/alfresco-global.properties', 'db.url\s*=.*', 'db.url=jdbc:' + db_type + '://' + db_host + ':' + db_port + '/' + db_name)


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

    print("nothing")
