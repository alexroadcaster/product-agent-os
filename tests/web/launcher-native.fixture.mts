process.send?.({type:'ready',port:41231,instanceId:process.env.PAOS_INSTANCE_ID??'fixture-instance',build:'paos-m1-0.1.0',pairingCode:'synthetic-pairing'});
process.on('message',(message:any)=>{
 if(message.type==='quit') {
  if(process.argv[2]==='no-ack')process.exit(0);
  else process.send?.({type:'stopped'},()=>process.exit(0));
 }
});
