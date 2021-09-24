function sample() {
  var min = 1 ;
  var max = 6 ;
  var a = Math.floor( Math.random() * (max + 1 - min) ) + min ;
  document.getElementById("example").innerHTML = a;
}