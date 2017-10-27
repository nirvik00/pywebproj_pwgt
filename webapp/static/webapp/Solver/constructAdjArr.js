/*
var adj=[];
adj.push("Entr,0,0,0,0,50");
adj.push("Eval,0,0,0,0,0");
adj.push("Nurse,0,0,0,0,0");
adj.push("Bath,0,0,0,0,0");
adj.push("Stair,0,0,0,0,0");
*/


function constructAdjArr(adj){
  /*
  * FOR THE SERVER : ADJACENCY ARRAY IS ALREADY
  * CONSTRUCTED AS PART OF READING THE FILE
  * THEREFORE JUST PUSH EACH LINE
  var names=[];
  var adjArr=[];
  for(var i=0; i<adj.length; i++){
    var n0=adj[i].split(",")[0];
    names.push(n0);
  }
  for(var i=0; i<adj.length; i++){
    var s=adj[i].split(",");
    var n0=adj[i].split(",")[0];
    for(var j=1; j<s.length; j++){
      var n1=names[j-1];
      var val=s[j];
      adjArr.push(n0+","+n1+","+val);      
    }
  }
  */
  var adjArr=[];
  for(var i=0; i<adj.length; i++){
    adjArr.push(adj[i]);
  }
  return adjArr;
}