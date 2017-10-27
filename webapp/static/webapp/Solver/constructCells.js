/*
var obj=[];
obj.push("Entr,1,255,0,0");
obj.push("Eval,1,0,255,0");
obj.push("Nurse,1,0,0,255");
obj.push("Bath,1,10,100,155");
obj.push("Stair,2,100,100,50");
*/

/*
*  CellObjClass
*/

function getNameList(){
  var name=[];
  var sum=0;
  for(var i=0; i<obj.length; i++){
    var s=obj[i].split(",");
    var n0=obj[i].split(",")[0];
    var num=obj[i].split(",")[2];
    for(var j=0; j<num; j++){
      name.push(n0);
      sum++;
    }
  }  
  return name;
}

function constructCellObj(names,obj){
  var n=names.length;
  var k=Math.floor(n/2);
  var cellObjArr=[];
  //a=length,b=depth,c=corridordepth,d=xoffset,e=yoffset
  var a0=int(50); 
  var b0=int(50);
  var c0=int(20); 
  var d0=int(100); 
  var e0=int(50);   
  var counter=0;
  for(var i=0; i<k; i++){
    var x=((i*a0)+d0);
    var y=e0;
    rect(x,y,a0,b0);
    var colr=[];    
    for(var j=0; j<obj.length; j++){     
      var s=obj[j].split(",")[0];
      if(s===(names[i])){        
        var re=int(obj[j].split(",")[3]);
        var gr=int(obj[j].split(",")[4]);
        var bl=int(obj[j].split(",")[5]);        
        colr=[re,gr,bl];
      }
    }
    var ce=new cell(counter,x,y,a0,b0,names[i],colr);
    cellObjArr.push(ce);
    counter++;
  }
  for(var i=k; i<n; i++){
    var x=(i-k)*a0+d0;
    var y=b0+c0+e0;
    rect(x,y,a0,b0);
    var colr=[];    
    for(var j=0; j<obj.length; j++){
      var s=obj[j].split(",")[0];
      if(s===(names[i])){
        var re=int(obj[j].split(",")[3]);
        var gr=int(obj[j].split(",")[4]);
        var bl=int(obj[j].split(",")[5]);
        colr=[re,gr,bl];
      }
    }
    var ce=new cell(counter,x,y,a0,b0,names[i],colr);
    cellObjArr.push(ce);
    counter++;
  }
  return cellObjArr;
}