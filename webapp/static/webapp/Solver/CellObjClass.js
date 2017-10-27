
function cell(id_, x_, y_, a_, b_, n_, c_){
  this.id=id_;
  this.x=x_;
  this.y=y_;
  this.a=a_;
  this.b=b_;
  this.name=n_;
  this.colr=c_;
  
  this.getId=function(){
    return this.id;
  }
  
  this.getX=function(){
    return this.x;
  }

  this.getY=function(){
    return this.y;
  }
  
  this.getA=function(){
    return this.a;
  }
  
  this.getB=function(){
    return this.b;
  }
  
  this.getName=function(){    
    return this.name;
  }
  
  this.setName=function(name_){    
    this.name=name_;
  }
  
  this.getColr=function(){
    return this.colr;
  }
  
  this.setColr=function(c_){
    this.colr=c_;
  }
  
  this.getMP=function(){
    var mpx=(this.x+this.a)/2;
    var mpy=(this.y+this.b)/2;
    var mp=[mpx,mpy];
    return mp;
  }
  
  this.display=function(){
    fill(255,0,0,50);
    rect(this.x,this.y,this.a, this.b);
    text(this.name,x,y);
  }
  
}