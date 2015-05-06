//Changes the width of 'target' based on the dx and the width of 'other' to compensate
function changeWidth(target, other, dx){
  //If the style.width hasn't been set yet, it needs to be set
  //The client width isn't exactly the same, so the offset is a rough estimation. This could be improved
  if(target.style.width==""){
    offset = 1.5;
    target.style.width = (target.clientWidth+offset)+'px';
    target.setAttribute('orgWidth',target.clientWidth+offset);
  }
  if(other.style.width==""){
    offset = 1.5;
    other.style.width = (other.clientWidth+offset)+'px';
    other.setAttribute('orgWidth',other.clientWidth+offset);
  }
  
  //Update the widths
  targetWidth = parseFloat(target.style.width.slice(0,-2));
  newTargetWidth = targetWidth+dx;
  otherWidth = parseFloat(other.style.width.slice(0,-2));
  newOtherWidth = otherWidth-dx;

  //Don't let either window get too small
  if(newTargetWidth > (target.getAttribute('orgWidth')*0.3) && newOtherWidth > (other.getAttribute('orgWidth')*0.3)){
    target.style.width = newTargetWidth + 'px';
    other.style.width = newOtherWidth + 'px';
  }
}

interact('#directory')
  .draggable({
    onmove: window.dragMoveListener
  })
  .resizable({
    edges: { right: true }
  })
  .on('resizemove', function (event) {
    var dir = event.target,
        code = $('#code')[0];

    changeWidth(dir,code,event.dx);

  });

interact('#code')
  .draggable({
    onmove: window.dragMoveListener
  })
  .resizable({
    edges: { right: true }
  })
  .on('resizemove', function (event) {
    var code = event.target,
        output = $('#output')[0];

    changeWidth(code,output,event.dx);

  });