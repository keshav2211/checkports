class checkports (
 $host_port_hash = hiera(checkports::host_port_hash),
 ){

$host_port_hash.each | String $host, Array $portlist| {
 $portlist.each | String $port | {
  porttest::tcp { "Testing $port on $host":
   target => $host,
   port   => $port,
  }
 }
}
}

