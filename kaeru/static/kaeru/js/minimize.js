//There are occasionally glitches where minimization does not work properly, not sure
//which situation causes it because could not repeat the error

var directory = $('#directory');
var code = $('#code');
var output = $('#output');

var maxDirButton = $('#max-directory-button');
var maxCodeButton = $('#max-code-button');
var maxOutputButton = $('#max-output-button');
var maxDirButton2 = $('#max-directory-button2');
var maxCodeButton2 = $('#max-code-button2');
var maxOutputButton2 = $('#max-output-button2');

var dirIsMin = false;
var codeIsMin = false;
var outputIsMin = false;

//Directory Section
$(function() {
    $('#min-directory-button').click(function() {
        if(!(codeIsMin&&outputIsMin)){
            dirIsMin = true;
            directory.toggleClass('small-2 hide');

            if(codeIsMin){
                output.toggleClass('small-10 small-12')
                maxDirButton2.removeClass('hide'); 
            }else if(outputIsMin){    
                code.toggleClass('small-10 small-12')
                maxDirButton.removeClass('hide');
            }else{
                code.toggleClass('small-3 small-5');
                maxDirButton.removeClass('hide');
            }    
        }
    });
});

//The maximize directory button in the code window is pressed
$(function() {
    maxDirButton.click(function() {
        dirIsMin = false;
        directory.toggleClass('hide small-2');

        if(outputIsMin){
            code.toggleClass('small-12 small-10');
        }else{
            code.toggleClass('small-5 small-3');
        }

        maxDirButton.addClass('hide');
    });
});

//The maximize directory button in the output window is pressed
$(function() {
    maxDirButton2.click(function() {
        dirIsMin = false;

        directory.toggleClass('hide small-2');

        if(codeIsMin){
            output.toggleClass('small-12 small-10')        
        }else{
            code.toggleClass('small-5 small-3');
        }

        maxDirButton2.addClass('hide');
    });
});


//Code Section
$(function() {
    $('#min-code-button').click(function() {
        if(!(dirIsMin&&outputIsMin)){
            codeIsMin = true;  
            if(dirIsMin){
                code.toggleClass('small-5 hide');
                output.toggleClass('small-7 small-12')
                maxCodeButton2.removeClass('hide');
                maxDirButton.addClass('hide');
                maxDirButton2.removeClass('hide');
            }else if(outputIsMin){    
                code.toggleClass('small-10 hide')
                directory.toggleClass('small-2 small-12')
                maxCodeButton.removeClass('hide');
                maxOutputButton2.addClass('hide');
                maxOutputButton.removeClass('hide');
            }else{
                code.toggleClass('small-3 hide');
                output.toggleClass('small-7 small-10')
                maxCodeButton2.removeClass('hide');
            }
        }    
    });
});

//The maximize code button in the directory windows is pressed
$(function() {
    maxCodeButton.click(function() {
        codeIsMin = false;
        if(outputIsMin){
            code.toggleClass('hide small-10');
            directory.toggleClass('small-12 small-2');
            maxOutputButton2.removeClass('hide');
            maxOutputButton.addClass('hide');
        }else{
            code.toggleClass('hide small-3');
            output.toggleClass('small-10 small-7')
        }
        maxCodeButton.addClass('hide');
    });
});

//The maximize code button in the code window is pressed
$(function() {
    maxCodeButton2.click(function() {
        codeIsMin = false;
        if(dirIsMin){
            code.toggleClass('hide small-5');
            output.toggleClass('small-12 small-7');
            maxDirButton.removeClass('hide');
            maxDirButton2.addClass('hide');
        }else{
            code.toggleClass('hide small-3');
            output.toggleClass('small-10 small-7')
        }
        maxCodeButton2.addClass('hide');
    });
});


//Output
$(function() {
    $('#min-output-button').click(function() {
        if(!(dirIsMin&&codeIsMin)){
            outputIsMin = true;  
            if(dirIsMin){
                output.toggleClass('small-7 hide');
                code.toggleClass('small-5 small-12')
                maxOutputButton2.removeClass('hide');
            }else if(codeIsMin){    
                output.toggleClass('small-10 hide')
                directory.toggleClass('small-2 small-12')
                maxOutputButton.removeClass('hide');
                maxCodeButton.addClass('hide');
                maxCodeButton.removeClass('hide');
            }else{
                output.toggleClass('small-7 hide');
                code.toggleClass('small-3 small-10')
                maxOutputButton2.removeClass('hide');
            }
        }    
    });
});

//The maximize output button in the directory window is pressed
$(function() {
    maxOutputButton.click(function() {
        outputIsMin = false;
        if(codeIsMin){
            output.toggleClass('hide small-10');
            directory.toggleClass('small-12 small-2');
            maxCodeButton2.removeClass('hide');
            maxCodeButton.addClass('hide');
        }else{
            output.toggleClass('hide small-7');
            code.toggleClass('small-10 small-3')
        }
        maxOutputButton.addClass('hide');
    });
});

//The maximize output button is pressed in the code window
$(function() {
    maxOutputButton2.click(function() {
        outputIsMin = false;
        if(dirIsMin){
            output.toggleClass('hide small-7');
            code.toggleClass('small-12 small-5');
        }else{
            output.toggleClass('hide small-7');
            code.toggleClass('small-10 small-3')
        }
        maxOutputButton2.addClass('hide');
    });
});