process.on('message',(message:any)=>{if(message.type==='quit')process.send?.({type:'stopped'},()=>process.exit(0));});
process.send?.({type:'ready',port:41231,instanceId:process.env.PAOS_INSTANCE_ID,build:'paos-m1-0.1.0',pairingCode:'synthetic-pairing'});
setTimeout(()=>process.send?.({type:'quit_requested'}),250);
setTimeout(()=>process.exit(3),2000).unref();
