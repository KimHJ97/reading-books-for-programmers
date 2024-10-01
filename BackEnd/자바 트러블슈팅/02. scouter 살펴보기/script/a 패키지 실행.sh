javac ./a/B.java
java -cp . a.B

java -javaagent:C:\Users\PC\Desktop\scouter\scouter\agent.java\scouter.agent.jar ^
-Dscouter.config=C:\Users\PC\Desktop\scouter\scouter\agent.java\conf\daemon.conf ^
-cp . a/B