/** GLOBALS */

// the max width and height for a page
MAX_WIDTH = screen.width;
MAX_HEIGHT = screen.height;

// the modes for adding elements
ADD_CENTER = "center";
ADD_CORNER = "corner";

// current width and height
windowx = 0;
windowy = 0;

// the page
page = undefined;


/** An element representing text */
var TextObject = function(text) {

	// private field holding the javascript element
	this.elem;

	/** sets the text that shows up */
	this.setText = function(text) {
		this.elem.nodeValue = text;
	}

	/** gets the text that shows up */
	this.getText = function() {
		return this.elem.nodeValue;
	}

	/** adds this object to the specified section */
	this.addToSection = function(section) {
		section.appendChild(this.elem);
	}

	/** removes this object from the specified section */
	this.removeFromSection = function(section) {
		section.removeChild(this.elem);
	}

	/** adds this object to the specified element */
	this.addToElement = function(element) {
		element.appendChild(this.elem);
	}

	/** removes this object from the specified element */
	this.removeFromElement = function(element) {
		element.removeChild(this.elem);
	}

	/** constructor for this object */
	this._constructor = function(text) {
		this.elem = document.createTextNode(text);
	}

	// deals with the constructor logic
	if (text == undefined) {
		this._constructor("");
	} else {
		this._constructor(text);
	}
}

/** An element representing a hyperlink text */
var HyperLinkObject = function(text, link) {

	// private field holding the javascript element
	this.elem;

	/** sets the text that shows up */
	this.setText = function(text) {
		this.elem.innerHTML = text;
	}

	/** gets the text that shows up */
	this.getText = function() {
		return this.elem.innerHTML;
	}

	/** sets the link */
	this.setLink = function(link) {
		this.elem.href = link;
	}

	/** gets the link */
	this.getLink = function() {
		return this.elem.href;
	}

	/** adds this object to the specified section */
	this.addToSection = function(section) {
		section.appendChild(this.elem);
	}

	/** removes this object from the specified section */
	this.removeFromSection = function(section) {
		section.removeChild(this.elem);
	}

	/** adds this object to the specified element */
	this.addToElement = function(element) {
		element.appendChild(this.elem);
	}

	/** removes this object from the specified element */
	this.removeFromElement = function(element) {
		element.removeChild(this.elem);
	}

	/** constructor */
	this._constructor = function() {
		this.elem = document.createElement("a");
	}

	this._constructorWithText = function(ptext) {
		this._constructor();
		this.elem.innerHTML = ptext;
	}

	this._constructorWithTextLink = function(ptext,plink) {
		this._constructorWithText(ptext);
		this.elem.href = plink;
	}

	if (text == undefined) {
		this._constructor();
	} else if (link == undefined) {
		this._constructorWithText(text)
	} else {
		this._constructorWithTextLink(text,link);
	}
}

/** An element representing a paragraph */
var ParagraphObject = function(ewidth, eheight) {

	// private field holding the javascript element
	this.elem;

	// the width
	this.ewidth;

	// the height
	this.eheight;

	// private fields denoting anchors
	this.anchortop = true;
	this.anchorbottom = false;
	this.anchorleft = true;
	this.anchorright = false;

	/** set anchors */
	this.setAnchors = function(top,right,bottom,left) {
		this.anchortop = top;
		this.anchorright = right;
		this.anchorbottom = bottom;
		this.anchorleft = left;
	}

	/** resize callback */
	this.resizeAnchor = function(newx, newy) {
		dx = newx - windowx;
		dy = newy - windowy;
		if (!isNaN(dx)) {
			if (this.anchorleft && this.anchorright) {
				right = windowx - parseInt(this.elem.style.left) - this.ewidth;
				this.ewidth = this.ewidth + dx;
				this.elem.style.width = this.ewidth;
				this.elem.style.left = newx - right - this.ewidth;
			} else if (this.anchorright) {
				right = windowx - parseInt(this.elem.style.left) - this.ewidth;
				this.elem.style.left = newx - right - this.ewidth;
			} else if (this.anchorleft) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				this.ewidth = this.ewidth + dx;
				this.elem.style.width = this.ewidth;
				this.elem.style.left = parseInt(this.elem.style.left) - dx/2;
			}

		}
		if (!isNaN(dy)) {
			if (this.anchortop && this.anchorbottom) {
				bottom = windowy - parseInt(this.elem.style.top) - this.eheight;
				this.eheight = this.eheight + dy;
				this.elem.style.height = this.eheight;
				this.elem.style.top = newy - bottom - this.eheight;
			} else if (this.anchorbottom) {
				bottom = windowy - parseInt(this.elem.style.top) - this.eheight;
				this.elem.style.top = newy - bottom - this.eheight;
			} else if (this.anchortop) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				this.eheight = this.eheight + dy;
				this.elem.style.height = this.eheight;
				this.elem.style.top = parseInt(this.elem.style.top) - dy/2;
			}
		}
	}

	/** adds this object to the specified section */
	this.addToSection = function(section, mode, x, y) {
		section.appendChild(this.elem);
		if (mode != undefined) {
			if (mode == ADD_CENTER) {
				this.elem.style.position = "absolute";
				this.elem.style.left = x - (this.ewidth/2);
				this.elem.style.top = y - (this.eheight/2);
			} else {
				this.elem.style.position = "absolute";
				this.elem.style.left = x;
				this.elem.style.top = y;
			}
		}
	}

	/** remove this object from the specified section */
	this.removeFromSection = function(section) {
		section.removeChild(this.elem);
	}

	/** adds a text object or hyperlink object */
	this.addText = function(textobject) {
		textobject.addToElement(this.elem);
	}

	/** removes a text object or hyperlink object */
	this.removeText = function(textobject) {
		textobject.removeFromElement(this.elem);
	}

	/** constructor */
	this._constructor = function() {
		this.elem = document.createElement("p");
		if (ewidth != undefined) {
			this.ewidth = ewidth;
		}
		if (eheight != undefined) {
			this.eheight = eheight;
		}
		this.elem.style.width = ewidth;
		this.elem.style.height = eheight;
	}

	this._constructor();
}

/** An element representing a button */
var ButtonObject = function(ewidth, eheight, giventext, givenfunc) {

	// private field holding the javascript element
	this.elem; 

	// private field holding a TextObject (text on the button)
	this.innerText;

	// the width
	this.ewidth;

	// the height
	this.eheight;

	// private field denoting children
	this.children = [];

	// private fields denoting anchors
	this.anchortop = true;
	this.anchorbottom = false;
	this.anchorleft = true;
	this.anchorright = false;

	/** set anchors */
	this.setAnchors = function(top,right,bottom,left) {
		this.anchortop = top;
		this.anchorright = right;
		this.anchorbottom = bottom;
		this.anchorleft = left;
	}

	/** resize callback */
	this.resizeAnchor = function(newx, newy) {
		dx = newx - windowx;
		dy = newy - windowy;
		if (!isNaN(dx)) {
			if (this.anchorleft && this.anchorright) {
				right = windowx - parseInt(this.elem.style.left) - this.ewidth;
				this.ewidth = this.ewidth + dx;
				this.elem.style.width = this.ewidth;
				this.elem.style.left = newx - right - this.ewidth;
			} else if (this.anchorright) {
				right = windowx - parseInt(this.elem.style.left) - this.ewidth;
				this.elem.style.left = newx - right - this.ewidth;
			} else if (this.anchorleft) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				this.ewidth = this.ewidth + dx;
				this.elem.style.width = this.ewidth;
				this.elem.style.left = parseInt(this.elem.style.left) - dx/2;
			}

		}
		if (!isNaN(dy)) {
			if (this.anchortop && this.anchorbottom) {
				bottom = windowy - parseInt(this.elem.style.top) - this.eheight;
				this.eheight = this.eheight + dy;
				this.elem.style.height = this.eheight;
				this.elem.style.top = newy - bottom - this.eheight;
			} else if (this.anchorbottom) {
				bottom = windowy - parseInt(this.elem.style.top) - this.eheight;
				this.elem.style.top = newy - bottom - this.eheight;
			} else if (this.anchortop) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				this.eheight = this.eheight + dy;
				this.elem.style.height = this.eheight;
				this.elem.style.top = parseInt(this.elem.style.top) - dy/2;
			}
		}
	}

	/** sets the innertext to the new innertext */
	this.setInnerText = function(innertext) {
		while(this.elem.hasChildNodes()) {
			this.elem.removeChild(this.elem.lastChild);
		}
		innertext.addToElement(this.elem);
		this.children.push(innertext);
		this.innerText = innertext;
	}

	/** gets the innertext */
	this.getInnerText = function() {
		return this.innerText;
	}

	/** sets the onclick function */
	this.setOnClick = function(func) {
		this.elem.onclick = func;
	}

	/** adds this object to the specified section */
	this.addToSection = function(section, mode, x, y) {
		section.appendChild(this.elem);
		if (mode != undefined) {
			if (mode == ADD_CENTER) {
				this.elem.style.position = "absolute";
				this.elem.style.left = x - (this.ewidth/2);
				this.elem.style.top = y - (this.eheight/2);
			} else {
				this.elem.style.position = "absolute";
				this.elem.style.left = x;
				this.elem.style.top = y;
			}
		}
	}

	/** remove this object from the specified section */
	this.removeFromSection = function(section) {
		section.removeChild(this.elem);
	}

	/** normal constructor */
	this._constructor = function() {
		this.elem = document.createElement("Button");
		if (ewidth != undefined) {
			this.ewidth = ewidth;
		}
		if (eheight != undefined) {
			this.eheight = eheight;
		}
		this.elem.style.width = ewidth;
		this.elem.style.height = eheight;
	}

	/** constructor with text specified */
	this._constructorWithText = function(text) {
		this._constructor()
		var translatedtext = new TextObject(giventext);
		this.setInnerText(translatedtext);
	}

	/** constructor with text and onclick specified */
	this._constructorWithTextandFunc = function(text,func) {
		this._constructorWithText(text);
		this.setOnClick(givenfunc);
	}

	// constructor logic
	if (giventext != undefined) {
		if (givenfunc != undefined) {
			this._constructorWithTextandFunc(giventext,givenfunc);
		} else {
			this._constructorWithText(giventext);
		}
	} else {
		this._constructor();
	}
}

/** An object denoting a radio button */
var RadioObject = function(ewidth, eheight, name, amount, orient) {

	// private field holding all the javascript radios
	this.elem = []

	// private field holdng all the javascript labels
	this.labels = []

	// private field holding all the br
	this.brs = []

	// private field holding the name of the radio
	this.rname = name;

	// private field denoting the orientation (vertical or horizontal)
	this.orientation;

	//private field denoting the number of options
	this.num;

	// the width
	this.ewidth;

	// the height
	this.eheight;

	// the fontsize
	this.fontsize = 14;

	// private fields denoting anchors
	this.anchortop = true;
	this.anchorbottom = false;
	this.anchorleft = true;
	this.anchorright = false;

	/** set anchors */
	this.setAnchors = function(top,right,bottom,left) {
		this.anchortop = top;
		this.anchorright = right;
		this.anchorbottom = bottom;
		this.anchorleft = left;
	}

	/** resize callback */
	this.resizeAnchor = function(newx, newy) {
		dx = newx - windowx;
		dy = newy - windowy;
		if (!isNaN(dx)) {
			if (this.anchorleft && this.anchorright) {
				//radios do not change width

			} else if (this.anchorright) {
				acc = 0;
				while (acc < this.elem.length) {
					right = windowx - parseInt(this.elem[acc].style.left) - this.ewidth;
					labelright = windowx - parseInt(this.labels[acc].style.left) - this.ewidth;
					this.elem[acc].style.left = newx - right - this.ewidth;
					this.labels[acc].style.left = newx - labelright - this.ewidth;
					acc = acc + 1;
				}
			} else if (this.anchorleft) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				//radios do not change width

			}

		}
		if (!isNaN(dy)) {
			if (this.anchortop && this.anchorbottom) {
				//radios do not change width

			} else if (this.anchorbottom) {
				acc = 0;
				while (acc < this.elem.length) {
					bottom = windowy - parseInt(this.elem[acc].style.top) - this.eheight;
					labelbottom = windowy - parseInt(this.labels[acc].style.top) - this.eheight;
					this.elem[acc].style.top = newy - bottom - this.eheight;
					this.labels[acc].style.top = newy - labelbottom - this.eheight;
					acc = acc + 1;
				}
			} else if (this.anchortop) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				//radios do not change width

			}
		}
		
	}

	/** add an additional option */
	this.addOption = function() {
		this.elem[this.num] = document.createElement("input");
		this.elem[this.num].type = "radio";
		this.elem[this.num].name = rname;
		this.labels[this.num] = document.createElement("label");
		this.labels[this.num].appendChild(this.elem[acc]);
		this.labels[this.num].innerHTML = "";
		this.elem[this.num].appendChild(this.labels[acc]);
		this.elem[this.num].style.width = ewidth;
		this.elem[this.num].style.height = eheight;	
		this.num += 1;
	}

	/** deletes the indexed option */
	this.deleteOption = function(num) {
		temp = num;
		while (temp < this.num - 1) {
			this.elem[temp] = this.elem[temp+1];
			this.labels[temp] = this.labels[temp+1];
			temp += 1;
		}
		this.num -= 1;
	}

	/** get number of options */
	this.getNumberOfOptions = function() {
		return this.num;
	}

	/** configure an option (important for setting value and label) */
	this.configureOption = function(index, value, shownText) {
		this.elem[index].value = value;
		this.labels[index].innerHTML = shownText;
	}

	/** sets the orientation of the radio */
	this.setOrientation = function(orient) {
		this.orientation = orient;
	}

	/** gets the orientation of the radio */
	this.getOrientation = function() {
		return this.orientation;
	}

	/** gets the value that's checked */
	this.getCheckedValue = function() {
		acc = 0;
		while (acc < this.num) {
			if (this.elem[acc].checked) {
				return this.elem[acc].value;
			}
			acc += 1;
		}
		return null;
	}

	/** add this to the specified section */
	this.addToSection = function(section, mode, x, y) {
		temp = 0;
		offsetx = 0;
		offsety = 0;
		offsetlabelx = 0;
		offsetlabely = 0;
		if (this.orientation == "vertical") {
			offsetlabelx = this.ewidth + this.fontsize;
			offsetlabely = this.eheight - this.fontsize;
		} else {
			offsetlabely = this.eheight - this.fontsize;
			offsetlabelx = this.ewidth + this.fontsize;
		}
		while (temp < this.getNumberOfOptions()) {
			section.appendChild(this.elem[temp]);
			section.appendChild(this.labels[temp]);
			if (mode != undefined) {
				if (mode == ADD_CENTER) {
					this.elem[temp].style.position = "absolute";
					this.elem[temp].style.left = x - (this.ewidth/2) + offsetx;
					this.elem[temp].style.top = y - (this.eheight/2) + offsety;
					this.labels[temp].style.position = "absolute";
					this.labels[temp].style.left = x - (this.ewidth/2) +offsetx +offsetlabelx;
					this.labels[temp].style.top = y - (this.eheight/2) +offsety +offsetlabely;
				} else {
					this.elem[temp].style.position = "absolute";
					this.elem[temp].style.left = x + offsetx;
					this.elem[temp].style.top = y + offsety;
					this.labels[temp].style.position = "absolute";
					this.labels[temp].style.left = x + offsetx +offsetlabelx;
					this.labels[temp].style.top = y + offsety +offsetlabely;
				}
			}
			if (this.orientation == "vertical") {
				var br = document.createElement("br");
				this.brs[temp] = br;
				section.appendChild(br);
				offsety += this.eheight;
			} else {
				offsetx += 2*this.ewidth;
			}
			temp += 1;
		}
	}

	/** remove this from the specified section */
	this.removeFromSection = function(section) {
		temp = 0;
		while (temp < this.getNumberOfOptions()) {
			section.removeChild(this.elem[temp]);
			section.removeChild(this.labels[temp]);
			if (this.orientation == "vertical") {
				section.removeChild(this.brs[temp]);
			}
			temp += 1;
		}
	}


	/** constructor */
	this._constructor = function(n) {
		this.rname = n;
	}

	/** constructor with amount and orientation */
	this._constructorWithAmountWithOrient = function(n,a,o) {
		if (ewidth != undefined) {
			this.ewidth = ewidth;
		}
		if (eheight != undefined) {
			this.eheight = eheight;
		}
		this.rname = n;
		this.num = a;
		acc = 0;
		while (acc < a) {
			this.elem[acc] = document.createElement("input");
			this.elem[acc].name = name;
			this.elem[acc].type = "radio";
			this.elem[acc].style.fontSize = 14;
			this.labels[acc] = document.createElement("label");
			this.labels[acc].appendChild(this.elem[acc]);
			this.labels[acc].innerHTML = "";
			this.elem[acc].appendChild(this.labels[acc]);
			this.elem[acc].style.width = ewidth;
			this.elem[acc].style.height = eheight;
			acc += 1;
		}
		this.orientation = o;
	}

	// constructor logic
	if (amount != undefined) {
		if (orient != undefined) {
			this._constructorWithAmountWithOrient(name,amount,orient);
		} else {
			this._constructorWithAmountWithOrient(name,amount,"vertical");
		}
	} else {
		this._constructor();
	}


}

/** An object denoting a textfield */
var TextFieldObject = function(ewidth,eheight,defaultvalue) {

	// private field denoting the javascript element
	this.elem;

	//private field denoting the name
	this.tname;

	// the width
	this.ewidth;

	// the height
	this.eheight;

	// private fields denoting anchors
	this.anchortop = true;
	this.anchorbottom = false;
	this.anchorleft = true;
	this.anchorright = false;

	/** set anchors */
	this.setAnchors = function(top,right,bottom,left) {
		this.anchortop = top;
		this.anchorright = right;
		this.anchorbottom = bottom;
		this.anchorleft = left;
	}

	/** resize callback */
	this.resizeAnchor = function(newx, newy) {
		dx = newx - windowx;
		dy = newy - windowy;
		if (!isNaN(dx)) {
			if (this.anchorleft && this.anchorright) {
				right = windowx - parseInt(this.elem.style.left) - this.ewidth;
				this.ewidth = this.ewidth + dx;
				this.elem.style.width = this.ewidth;
				this.elem.style.left = newx - right - this.ewidth;
			} else if (this.anchorright) {
				right = windowx - parseInt(this.elem.style.left) - this.ewidth;
				this.elem.style.left = newx - right - this.ewidth;
			} else if (this.anchorleft) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				this.ewidth = this.ewidth + dx;
				this.elem.style.width = this.ewidth;
				this.elem.style.left = parseInt(this.elem.style.left) - dx/2;
			}

		}
		if (!isNaN(dy)) {
			if (this.anchortop && this.anchorbottom) {
				bottom = windowy - parseInt(this.elem.style.top) - this.eheight;
				this.eheight = this.eheight + dy;
				this.elem.style.height = this.eheight;
				this.elem.style.top = newy - bottom - this.eheight;
			} else if (this.anchorbottom) {
				bottom = windowy - parseInt(this.elem.style.top) - this.eheight;
				this.elem.style.top = newy - bottom - this.eheight;
			} else if (this.anchortop) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				this.eheight = this.eheight + dy;
				this.elem.style.height = this.eheight;
				this.elem.style.top = parseInt(this.elem.style.top) - dy/2;
			}
		}

	}


	/** get the value of this textfield */
	this.getValue = function() {
		return this.elem.nodeValue;
	}

	/** set the value of this textfield */
	this.setValue = function(value) {
		this.elem.nodeValue = value;
	}

	/** adds this object to the specified section */
	this.addToSection = function(section, mode, x, y) {
		section.appendChild(this.elem);
		if (mode != undefined) {
			if (mode == ADD_CENTER) {
				this.elem.style.position = "absolute";
				this.elem.style.left = x - (this.ewidth/2);
				this.elem.style.top = y - (this.eheight/2);
			} else {
				this.elem.style.position = "absolute";
				this.elem.style.left = x;
				this.elem.style.top = y;
			}
		}
		right = windowx - parseInt(this.elem.style.left) - this.ewidth;


	}

	/** remove this object from the specified section */
	this.removeFromSection = function(section) {
		section.removeChild(this.elem);
	}

	/** constructor */
	this._constructor = function() {
		this.elem = document.createElement("textarea");
		if (ewidth != undefined) {
			this.ewidth = ewidth;
		}
		if (eheight != undefined) {
			this.eheight = eheight;
		}
		this.elem.style.width = ewidth;
		this.elem.style.height = eheight;
	}

	/** constructor with default value */
	this._constructorWithValue = function(value) {
		this._constructor();
		this.elem.value = value;
	}

	// constructor logic
	if (defaultvalue != undefined) {
		this._constructorWithValue(defaultvalue);
	} else {
		this._constructor();
	}

}

/** An object denoting a break */
var BreakObject = function() {
	// private field holding the javascript element
	this.elem;

	/** resize callback */
	this.resizeAnchor = function(newx, newy) {

	}

	/** adds this object to the specified section */
	this.addToSection = function(section, mode, x, y) {
		section.appendChild(this.elem);
	}

	/** removes this object from the specified section */
	this.removeFromSection = function(section) {
		section.removeChild(this.elem);
	}

	/** constructor for this object */
	this._constructor = function() {
		this.elem = document.createElement("br");
	}

	// deals with the constructor logic
	this._constructor();
}

/** An object denoting a Section */
var Section = function(swidth,sheight,isform) {

	// private field denoting the javascript element
	this.sect;

	// private field denoting if this is a form
	this.isform;

	// private field denoting the submit button
	this.submitbutton;
	
	// the width
	this.swidth;

	// the height
	this.sheight;

	// private field denoting children
	this.children = [];

	// private fields denoting anchors
	this.anchortop = true;
	this.anchorbottom = false;
	this.anchorleft = true;
	this.anchorright = false;

	/** set anchors */
	this.setAnchors = function(top,right,bottom,left) {
		this.anchortop = top;
		this.anchorright = right;
		this.anchorbottom = bottom;
		this.anchorleft = left;
	}

	/** resize callback */
	this.resizeAnchor = function(newx, newy) {
		dx = newx - windowx;
		dy = newy - windowy;
		if (!isNaN(dx)) {
			if (this.anchorleft && this.anchorright) {
				right = windowx - parseInt(this.elem.style.left) - this.ewidth;
				this.ewidth = this.ewidth + dx;
				this.elem.style.width = this.ewidth;
				this.elem.style.left = newx - right - this.ewidth;
			} else if (this.anchorright) {
				right = windowx - parseInt(this.elem.style.left) - this.ewidth;
				this.elem.style.left = newx - right - this.ewidth;
			} else if (this.anchorleft) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				this.ewidth = this.ewidth + dx;
				this.elem.style.width = this.ewidth;
				this.elem.style.left = parseInt(this.elem.style.left) - dx/2;
			}

		}
		if (!isNaN(dy)) {
			if (this.anchortop && this.anchorbottom) {
				bottom = windowy - parseInt(this.elem.style.top) - this.eheight;
				this.eheight = this.eheight + dy;
				this.elem.style.height = this.eheight;
				this.elem.style.top = newy - bottom - this.eheight;
			} else if (this.anchorbottom) {
				bottom = windowy - parseInt(this.elem.style.top) - this.eheight;
				this.elem.style.top = newy - bottom - this.eheight;
			} else if (this.anchortop) {
				//CHANGE if no longer using top/left for javascript locations
			} else {
				this.eheight = this.eheight + dy;
				this.elem.style.height = this.eheight;
				this.elem.style.top = parseInt(this.elem.style.top) - dy/2;
			}
		}
		for (i = 0; i < this.children.length; i ++) {
			this.children[i].resizeAnchor(newx, newy);
		}
	}


	/** append an element to this section */
	this.appendElement = function(element, mode, x, y) {
		this.children.push(element);
		element.addToSection(this.sect, mode, x, y);
	}

	/** append a section to this section */
	this.appendSection = function(section, mode, x, y) {
		this.children.push(section);
		section.addToSection(this.sect, mode, x, y);
	}

	/** remove an element from this section */
	this.removeElement = function(element) {
		var index = this.children.indexOf(element);
		this.children = this.children.splice(index,1);
		element.removeFromSection(this.sect);
	}

	/** remove a section from this section */
	this.removeSection = function(section) {
		var index = this.children.indexOf(section);
		this.children = this.children.splice(index,1);
		section.removeFromSection(this.sect);
	}

	/** adds this object to the specified section */
	this.addToSection = function(section, mode, x, y) {
		section.appendChild(this.sect);
		if (mode != undefined) {
			if (mode == ADD_CENTER) {
				this.sect.style.position = "absolute";
				this.sect.style.left = x - (this.swidth/2);
				this.sect.style.top = y - (this.sheight/2);
			} else {
				this.sect.style.position = "absolute";
				this.sect.style.left = x;
				this.sect.style.top = y;
			}
		}
	}

	/** removes this object from the specified section */
	this.removeFromSection = function(section) {
		section.removeChild(this.sect);
	}

	/** add an action */
	this.addFormAction = function(link) {
		if (this.isform) {
			this.sect.action = link;
		}
	}

	/** add a break */
	this.addBreak = function() {
		var breakobj = new BreakObject();
		this.appendElement(breakobj);
		return breakobj;
	}

	/** add a submit button to form */
	this.addSubmit = function(customonclick) {
		if (this.isform) {
			this.submitbutton = document.createElement("input");
			this.submitbutton.type = "submit";
			this.submitbutton.value = "Submit";
			this.sect.appendChild(this.submitbutton);
			if (customonclick != undefined) {
				this.submitbutton.onclick = customonclick;	
			}
		}
	}

	/** constructor */
	this._constructor = function(isform) {
		this.isform = isform;
		if (isform) {
			this.sect = document.createElement("form");
		} else {
			this.sect = document.createElement("div");
		}
		if (swidth != undefined) {
			this.swidth = swidth;
		}
		if (sheight != undefined) {
			this.sheight = sheight;
		}
		this.sect.style.width = swidth;
		this.sect.style.height = sheight;
	}

	// construction logic
	if (isform == undefined) {
		this._constructor(false);
	} else {
		this._constructor(isform);
	}
}

/** An object denoting a page */
var Page = function(pwidth, pheight, title) {

	// title of the page
	this.title;
	
	// the root section
	this.root;

	// the width
	this.pwidth = MAX_WIDTH;

	// the height
	this.pheight = MAX_HEIGHT;

	/** getter for width */
	this.getWidth = function() {
		return this.pwidth;
	}

	/** getter for height */
	this.getHeight = function() {
		return this.pheight;
	}

	/** sets the title */
	this.setTitle = function(title) {
		document.title = title;
		this.title = title;
	}

	/** gets the title */
	this.getTitle = function() {
		return this.title;
	}

	/** add an element to page */
	this.appendElement = function(item, mode, x, y) {
		this.root.appendElement(item, mode, x, y);
	}

	/** remove an element from the page */
	this.removeElement = function(item) {
		this.root.removeElement(item);
	}

	/** add a section to page */
	this.appendSection = function(item, mode, x, y) {
		this.root.appendSection(item, mode, x, y);
	}

	/** remove a section from the page */
	this.removeSection = function(item) {
		this.root.removeSection(item);
	}

	/** normal constructor */
	this._constructor = function() {
		if (pwidth != undefined) {
			this.pwidth = pwidth;
		}
		if (pheight != undefined) {
			this.pheight = pheight;
		}
		window.resizeTo(this.pwidth,this.pheight);
		windowx = window.innerWidth;
		windowy = window.innerHeight;
		this.root = new Section(false,swidth=this.pwidth,sheight=this.pheight);
		this.root.addToSection(document.body);
		page = this;


		window.onresize = function () {
			page.root.resizeAnchor(window.innerWidth, window.innerHeight);
			page.pwidth += window.innerWidth - windowx;
			page.pheight += window.innerHeight - windowy;
			windowx = window.innerWidth;
			windowy = window.innerHeight;
		}


	}

	/** constructor with specified title */
	this._constructorWithTitle = function(title) {
		document.title = title;
		this.title = title;
		this._constructor();
	}

	// construction logic
	if (title != undefined) {
		this._constructorWithTitle(title);
	} else {
		this._constructor();
	}



}

