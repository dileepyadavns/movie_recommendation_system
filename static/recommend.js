$(function() {
    // Button will be disabled until we type anything inside the input field
    const source = document.getElementById('autoComplete');
    const inputHandler = function(e) {
      if(e.target.value==""){
        $('.movie-button').attr('disabled', true);
      }
      else{
        $('.movie-button').attr('disabled', false);
      }
    }
    source.addEventListener('input', inputHandler);
  
    $('.movie-button').on('click',function(){
      var my_api_key = '5492165c61b1a21c06eb3a3b578a6339';
      var title = $('.movie').val();
      if (title=="") {
        $('.results').css('display','none');
        $('.fail').css('display','block');
      }
      else{
        load_details(my_api_key,title);
      }
    });
  });
  
  // will be invoked when clicking on the recommended movies
  function recommendcard(e){
    var my_api_key = '5492165c61b1a21c06eb3a3b578a6339';
    var title = e.getAttribute('title'); 
    load_details(my_api_key,title);
  }
  
  // get the basic details of the movie from the API (based on the name of the movie)
  function load_details(my_api_key,title){
    $.ajax({
      type: 'GET',
      url:'https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+title,
  
      success: function(movie){
        if(movie.results.length<1){
          $('.fail').css('display','block');
          $('.results').css('display','none');
          $("#loader").delay(500).fadeOut();
        }
        else{
          $("#loader").fadeIn();
          $('.fail').css('display','none');
          $('.results').delay(1000).css('display','block');
          var movie_id = movie.results[0].id;
          var movie_title = movie.results[0].original_title;
          movie_recs(movie_title,movie_id,my_api_key);
        }
      },
      error: function(){
        alert('Invalid Request');
        $("#loader").delay(500).fadeOut();
      },
    });
  }
  
  // passing the movie name to get the similar movies from python's flask
  function movie_recs(movie_title,movie_id,my_api_key){
    $.ajax({
      type:'POST',
      url:"/similarity",
      data:{'name':movie_title},
      success: function(recs){
        if(recs=="Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies"){
          $('.fail').css('display','block');
          $('.results').css('display','none');
          $("#loader").delay(500).fadeOut();
        }
        else {
          $('.fail').css('display','none');
          $('.results').css('display','block');
          var movie_arr = recs.split('---');
          var arr = [];
          for(const movie in movie_arr){
            arr.push(movie_arr[movie]);
          }
          get_movie_details(movie_id,my_api_key,arr,movie_title);
        }
      },
      error: function(){
        alert("error recs");
        $("#loader").delay(500).fadeOut();
      },
    }); 
  }
  
  // get all the details of the movie using the movie id.
  function get_movie_details(movie_id,my_api_key,arr,movie_title) {
    $.ajax({
      type:'GET',
      url:'https://api.themoviedb.org/3/movie/'+movie_id+'?api_key='+my_api_key,
      success: function(movie_details){
        show_details(arr,my_api_key);
      },
      error: function(){
        alert("API Error!");
        $("#loader").delay(500).fadeOut();
      },
    });
  }
  
  // // passing all the details to python's flask for displaying and scraping the movie reviews using imdb id
  function show_details(arr,my_api_key){
   
    arr_poster = get_movie_posters(arr,my_api_key);
    
    details = {
     
        'rec_movies':JSON.stringify(arr),
        'rec_posters':JSON.stringify(arr_poster),
    }
  
    $.ajax({
      type:'POST',
      data:details,
      url:"/recommend",
      dataType: 'html',
      complete: function(){
        $("#loader").delay(500).fadeOut();
      },
      success: function(response) {
        $('.results').html(response);
        $('#autoComplete').val('');
        $(window).scrollTop(0);
      }
    });
  }
  
  
  // getting posters for all the recommended movies
  function get_movie_posters(arr,my_api_key){
    var arr_poster_list = []
    for(var m in arr) {
      $.ajax({
        type:'GET',
        url:'https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+arr[m],
        async: false,
        success: function(m_data){
          arr_poster_list.push('https://image.tmdb.org/t/p/original'+m_data.results[0].poster_path);
        },
        error: function(){
          alert("Invalid Request!");
          $("#loader").delay(500).fadeOut();
        },
      })
    }
    return arr_poster_list;
  }
  
