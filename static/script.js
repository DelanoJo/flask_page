// script.js
alert("Connected!");

$(function() {

$( 'li.draggable').draggable( {
        opacity: .6,
        create: function(){$(this).data('position',$(this).position())},
        cursorAt:{left:15},
        cursor:'move',
        start:function(){$(this).stop(true,true)}
    });

    $('.a-side').find('li.droppable').droppable({
        drop:function(event, ui){

            var $target = $(this);
            var prevName = $target.data('name');
            var $dragged = $(ui.draggable).removeAttr('style');

            $target.data('name', prevName + ':' + $dragged.data('name'));
            $target.attr('data-name', prevName + ':' + $dragged.data('name'));
            $target.addClass('joined');
            $target.append('<div data-name="' + $dragged.data('name') + '">' + $dragged.html() + '</div>');
            $target.droppable('destroy');



            }

        }
    });

    $('#save').on('click', function(e) {
        var list = [];
        $('.droppable').each(function(el) {
            list.push($(this).data('name'));
        });
        $.ajax({
            url: 'asdf',
            method: 'POST',
            data: {
                mapping: list
            }
        }).success(function(){
            alert('saved!');
        }).fail(function() {
            alert('saved failed.');
        });
    })
 });









