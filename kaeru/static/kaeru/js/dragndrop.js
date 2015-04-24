interact('#directory')
  .draggable({
    onmove: window.dragMoveListener
  })
  .resizable({
    edges: { left: true, right: true, bottom: true, top: true }
  })
  .on('resizemove', function (event) {
    var target = event.target,
        x = (parseFloat(target.getAttribute('data-x')) || 0),
        y = (parseFloat(target.getAttribute('data-y')) || 0);

    // update the element's style
    target.style.width  = event.rect.width + 'px';
    target.style.height = event.rect.height + 'px';

    //$('#code')[0]
    $('#code')[0].style.width = event.rect.width - 'px';

    // translate when resizing from top or left edges
    x += event.deltaRect.left;
    y += event.deltaRect.top;

    //not sure if this is necessary...
    //target.style.webkitTransform = target.style.transform =
     //   'translate(' + x + 'px,' + y + 'px)';
  });