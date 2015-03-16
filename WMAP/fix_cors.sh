#!/usr/bin/env bash

echo "**";
echo "** Tomcat";
echo "** Add config info to enable CORS";
echo "**";

read -r -d '' CORS_STRING << EOM

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
