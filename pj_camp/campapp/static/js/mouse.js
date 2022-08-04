let isClicked = false; 
var map = "";
function mouseClick( changeImgPath ) 
{ 
   isClicked = true; 
   map = changeImgPath;
   document.getElementById("Map").src = changeImgPath; 
} 
function mouseOver( changeImgPath ) 
{ 
    document.getElementById("Map").src = changeImgPath; 
} 
function mouseOut( changeImgPath ) 
{ 
   if( isClicked == false ) 
   { 
      document.getElementById("Map").src = changeImgPath; 
   }else{
      document.getElementById("Map").src = map; 
   } 
} 