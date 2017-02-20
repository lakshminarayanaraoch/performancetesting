node {
  stage 'Run JMeter Test'
  sh 'jmeter.sh -n -t /root/apache-jmeter-3.0/bin/Tmobile_search.jmx -l /root/results/sampleresult_tombile7.jtl'
}