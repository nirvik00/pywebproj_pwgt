var global_adjArr=[];var nameArr=[];
var cellObjArr=[];//class -> CellObjClass
var ite_fitness;
var ite_iniArr=[]; 
var funcArr=[];
var nameArr=[];
var global_fitness=10000;
/*
var adj=[];
adj.push("Entr,0,10,10,10,10");
adj.push("Eval,0,10,0,0,0");
adj.push("Nurse,0,0,-50,10,0");
adj.push("Bath,0,0,0,-50,0");
adj.push("Stair,0,0,0,0,-50");

var obj=[];
obj.push("Entr,5000,1,255,0,0");
obj.push("Eval,7500,5,0,255,0");
obj.push("Nurse,6700,2,0,0,255");
obj.push("Bath,4873,2,10,100,155");
obj.push("Stair,5454,2,100,155,10");
*/
function setup() {  
  createCanvas(1000,700);
  background(255);
  rect(25,25,450,200);
  stroke(0);
  text("Click to run program", 200, 125);
  global_adjArr=constructAdjArr(adj);//constructAdjArr
  nameArr=getNameList();//constructCells
  cellObjArr=constructCellObj(nameArr,obj);//constructCells  
  ite_iniArr=cellObjArr;
  var f0=fitness(ite_iniArr,global_adjArr);
  ite_fitness=f0;
  console.log("ok initialized");
  //console.log(ite_fitness);
  console.log("adjArr"+global_adjArr);
  //console.log("cellobj"+cellObjArr);
}

function draw() {
 /*
 *  go via mouseClicked()
 */
}
function mouseClicked(){
  var counter=0;
  while(counter<100){
    var finCells=swap(ite_iniArr,global_adjArr);
    var f1=fitness(finCells,global_adjArr);
    if(f1<ite_fitness+1 && counter<99){      
      ite_iniArr=finCells;
      ite_fitness=f1;
      break;
    }
    counter++;    
  }  
  
  console.log(ite_fitness,counter);
  if(counter<100){
    display(ite_iniArr,counter);
  }
  strokeWeight(1);
  fill(0);
  noFill();
  
}

function displayInfo(counter){
  strokeWeight(1);
  stroke(0);
  fill(0);  
  text("number of iterations: "+counter,100,300);  
}

function display(cellArr, counter){  
  background(255);
  fill(255);
  rect(0,0,1000,500);
  stroke(0);
  strokeWeight(1);
  var arr=cellArr;
  var n=int(arr.length);  
  for(var i=0; i<arr.length; i++){
    var ce=arr[i];
    var colr=arr[i].getColr();
    fill(colr[0],colr[1],colr[2]);    
    rect(ce.x,ce.y,ce.a,ce.b);
    fill(0);
    strokeWeight(.5);
    text(ce.getName(),ce.x,ce.y);
    noFill();
  }
  displayInfo(counter);
}