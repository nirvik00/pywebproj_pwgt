

function swap(cellObjArr, adjArr){
  var iniCells=[];
  var finCells=[];
  for(var i=0; i<cellObjArr.length;i++){
    finCells.push(cellObjArr[i]);
  }
  for(var i=0; i<cellObjArr.length;i++){
    iniCells.push(cellObjArr[i]);
  }
  var u=int(random(finCells.length-1));
  var v=int(random(finCells.length-1));  
  var nu=iniCells[u].getName();
  var nv=iniCells[v].getName();
  var cu=iniCells[u].getColr();
  var cv=iniCells[v].getColr();
  
  finCells[u].setName(nv);
  finCells[v].setName(nu);
  finCells[u].setColr(cv);
  finCells[v].setColr(cu);
  
  var f0=fitness(ite_iniArr,global_adjArr);
  var f1=fitness(finCells,global_adjArr);
  
  if(f0>f1){
    return finCells;
  }else{
    return iniCells;
  }
}

function fitness(arr, adjArr){
  var sum=0;
  for(var i=0; i<arr.length; i++){
    var nu=arr[i].getName();
    var mp0=arr[i].getMP();
    for(var j=0; j<arr.length; j++){
      var nv=arr[j].getName();
      var mp1=arr[j].getMP();
      var d=di(mp0,mp1);
      var val=findAdjVal(nu,nv,adjArr)*d;
      //console.log(nu,nv,val);
      sum+=val;
    }
  }
  return sum;
}

function findAdjVal(a,b,adjArr){
  /*
  *  string input 'a' is the first field and 'b' 2nd field
  */  
  var val=10000;
  for(var i=0; i<adjArr.length; i++){
    var u=adjArr[i].split(",")[0];
    var v=adjArr[i].split(",")[1];
    //console.log(u,v,a,b);
    if((u===a && v===b)||(u===b && v===a)){      
      val=int(adjArr[i].split(",")[2]);
      break;
    }
  }
  if(val!=10000){
    return val;
  }else{
    return 0;
  }
}

function di(p,q){
  var d=sqrt(((p[0]-q[0])*(p[0]-q[0]))+((p[1]-q[1])*(p[1]-q[1])));
  return d;
}