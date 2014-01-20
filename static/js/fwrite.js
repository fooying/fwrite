var loading_data = false;
var stop_load = false;
var columns_list = new Array();
var cur_page_a = 1;
var cur_page_c = 1;
var base_url = 'http://'+ location.host;
var ifarticle = false;


$(document).ready(function () {
    var split_str = location.href.split('/article/');
    if (split_str[1]){
        ifarticle = true;
        
    }
    $('#left_panel .nav_container ul').css('height', ($(window).height() - $('#left_panel .nav_container').offset()['top']));
    
    $(document).on('click', 'a.show_comment', function () {
        $('a.show_comment').removeClass('current');
        
        $(this).addClass('current');
        $('#data_lister').empty();
        ifarticle = true;
        var column_id = $(this).attr('columns_id');
        cur_page_a = 1;
        load_articles_list(column_id);
        $(".back").css("display","block");
        
        return false;
    });
    
    $('#data_lister').scroll(function() {
         if (($(this)[0].scrollTop + $(this).height()) >= $(this)[0].scrollHeight && loading_data == false && stop_load == false)
         {  
            if (ifarticle){
                load_articles_list(column_id);
            }
            else{
                load_columns_list();
            }
         }
    });
    
    if (ifarticle){
        load_articles_list(column_id);
    }
    else{
        load_columns_list();
    }

});

function load_columns_list()
{
    $('#data_lister').append('<li class="loading">Loading...</li>');
            
    loading_data = true;        
    $.getJSON(base_url + '/ajax/columns?page=' + cur_page_c, function(data) {
        
        if (data == '')
        {
            stop_load = true;
        }
        
        $('#data_lister li.loading').remove();
                
        $.each(data.columns, function (i, a) {
                $('#data_lister').append('<li>' +
                    '<a href="javascript:;" class="show_comment" columns_id="' + a['key'] + '">' +
                        '<h2>' + a['name'] + '</h2>' +
                    '</a>' + 
            '</li>');
        });
                
        loading_data = false;       
        cur_page_c++;
    });
}

function load_articles_list(column_id)
{
    $(".back").css("display","block");
    $('#data_lister').append('<li class="loading">Loading...</li>');
            
    loading_data = true;        
    $.getJSON(base_url + '/ajax/articles?page=' + cur_page_a +'&coumn_key=' + column_id, function(data) {
        
        if (data == '')
        {
            stop_load = true;
        }
        
        $('#data_lister li.loading').remove();
                
        $.each(data.articles, function (i, a) {
                $('#data_lister').append('<li>' +
                    '<a href="/article/' + a['key'] + '" target="_self" >' +
                        '<h2>' + a['title'] + '</h2>' +
                    '</a>' + 
            '</li>');
        });
                
        loading_data = false;       
        cur_page_a++;
    });
}

function back()
{
    $(".back").css("display","none");
    $('#data_lister').empty();
    ifarticle = false;
    cur_page_c = 1;
    load_columns_list();

}
