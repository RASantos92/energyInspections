$(function(){
    console.log("test")
    $('#buildCode2,#buildCode3').hide();
})
$('#slideToggle1').click(function(){
    console.log("slide test 1")
    $('#buildCode1').slideToggle();
})
$('#slideToggle2').click(function(){
    $('#buildCode2').slideToggle();
})
$('#slideToggle3').click(function(){
    $('#buildCode3').slideToggle();
})