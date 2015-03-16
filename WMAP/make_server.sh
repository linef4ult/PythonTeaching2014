#!/bin/bash
echo "**";
echo "** Bash script to download/install/configure Apache, PostgreSQL, PostGIS and Geoserver on a Ununtu Linux server.";
echo "**";
echo "** Mark Foley, January 2014.";
echo "**";

# Check that script run as root
if ! [ $UID = 0 ]; then
	echo "**";
	echo "** This script should be run as root. Exiting now.";
	echo "**";
	exit 1;
fi


echo "**";
echo "** Update existing package repositories and packages";
echo "**";

apt-get update -y
apt-get upgrade -y

echo "**";
echo "** Packages needed";
echo "**";

echo "**";
echo "** Apache web server";
echo "**";
apt-get install apache2 -y

echo "**";
echo "** PostgreSQL 9.x";
echo "**";
apt-get install postgresql -y

echo "**";
echo "** PostGIS 2.x -- note the '*'";
echo "**";
apt-get install postgis* -y

echo "**";
echo "** Tomcat servlet container";
echo "**";
apt-get install tomcat7 -y

echo "**";
echo "** Unzip";
echo "**";
apt-get install unzip -y

echo "**";
echo "** phppgadmin - Web-bbased admin interface for PostgreSQL";
echo "**";
apt-get install phppgadmin -y

echo "**";
echo "** geoserver - get it, unzip it and copy war file to appropriate directory so that Tomcat can see it.";
echo "**";
wget http://sourceforge.net/projects/geoserver/files/latest/download?source=files -O geoserver.zip
unzip geoserver.zip
cp -v geoserver.war /var/lib/tomcat7/webapps/

echo "**";
echo "** Adjust configuration files";
echo "**";
echo "** For Ubuntu 14.10 edit /etc/apache2/apache2.conf and add the following line to it:";
echo "** Include /etc/apache2/conf.d/phppgadmin";
echo "**";
./replace_str.py -a /etc/apache2/apache2.conf -n "Include /etc/apache2/conf.d/phppgadmin"

echo "**";
echo "** phppgadmin";
echo "** Comment out (add # at beginning of line) allow from 127.0.0.0/255.0.0.0 ::1/128 and remove # from the line below it, allow from all.";
echo "**";
./replace_str.py -r /etc/apache2/conf.d/phppgadmin -n "# allow from 127.0.0.0/255.0.0.0 ::1/128" -s "allow from 127.0.0.0/255.0.0.0 ::1/128"
./replace_str.py -r /etc/apache2/conf.d/phppgadmin -n "allow from all" -s "# allow from all"

echo "**replace $conf['extra_login_security'] = true; with $conf['extra_login_security'] = false;";
./replace_str.py -r /etc/phppgadmin/config.inc.php -n "$conf['extra_login_security'] = false;" -s "$conf['extra_login_security'] = true;"

echo "**";
echo "** PostgreSQL";
echo "** add line: host    all             all             0.0.0.0/0               md5";
./replace_str.py -a /etc/postgresql/9.3/main/pg_hba.conf -n "host    all             all             0.0.0.0/0               md5"

echo "** replace # listen_addresses = 'localhost' with listen_addresses = '*'";
./replace_str.py -r /etc/postgresql/9.3/main/postgresql.conf -n "listen_addresses = '*'" -s "#listen_addresses = 'localhost'"

echo "** Tomcat";
echo "** Add config info to enable CORS";
echo "**";

read -r -d '' CORS_STRING << EOM

<!-- Added filters to handle CORS requests - MF March 2015-->

  <filter>
    <filter-name>CorsFilter</filter-name>
    <filter-class>org.apache.catalina.filters.CorsFilter</filter-class>
    <init-param>
      <param-name>cors.allowed.origins</param-name>
      <param-value>*</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>CorsFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>


</web-app>
EOM

./replace_str.py -r /etc/tomcat7/web.xml -s "</web-app>" -n "$CORS_STRING";


echo "**";
echo "** Restart PostgreSQL, Apache and Tomcat so that these changes are activated";
echo "**";
service postgresql restart
service apache2 restart
service tomcat7 restart


echo "**";
echo "** Make your first spatial database";
echo "** Make a new databse user ($USER), connect and create database called 'firstspatial'";
echo "**";
sudo -u postgres createuser --superuser $USER
createdb -U $USER firstspatial

echo "**";
echo "** Add postgis and topology extensions";
echo "**";
psql -U $USER -d firstspatial -c "CREATE EXTENSION postgis;"
psql -U $USER -d firstspatial -c "CREATE EXTENSION postgis_topology;"

echo "**-----------------------------------------------------";
echo "** You need to change the database password for $USER";
echo "** Please enter this now.";
echo "**-----------------------------------------------------";
psql -U $USER -d firstspatial -c "\password"

echo "**";
echo "** FINISHED";
echo "**";
