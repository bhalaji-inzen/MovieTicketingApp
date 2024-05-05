Vue.component('index',{
    template : `
    <div>
    <div v-for="theatre in theatre_info">
        <div class="border container">
        <h3>Theatre : {{theatre['theatre_name']}}</h3>
        <p>{{theatre['theatre_place']}} - {{theatre['theatre_location']}}</p>
            <div v-if="isadmin === 'True'">
            <a class="btn btn-warning" v-bind:href="'/edit_theatre/' + theatre['theatre_id']">Edit Theatre</a>
            <a class="btn btn-danger"  @click="delete_theatre(theatre['theatre_id'])">Delete Theatre</a>
            <a class="btn btn-success" v-bind:href="'/theatre_report/' + theatre['theatre_id']">Export as csv</a>
            </div>
            <h4>Shows</h4>
            <div class="border" v-for="show in theatre['shows']">
            <div class="border">
            <h2>Movie : {{show['show_name']}}</h2>
            <p>Show starts in:{{show['show_start_timing']}}</p>
            <div v-if="isadmin === 'True'">
                <a class="btn btn-warning" v-bind:href="'/'+theatre['theatre_id'] + '/edit_show/' + show['show_id']">Edit Show</a>
                <a class="btn btn-danger" @click="delete_show(theatre['theatre_id'],show['show_id'])">Delete Show</a>
            </div>
            <div v-if="isadmin === 'False'">
                <a class="btn btn-outline-danger" v-bind:href="'/book_show/'+ cur_user_id + '/' + show['show_id']">Book show</a>
            </div>
            </div>
            </div>
        <div v-if="isadmin === 'True'">
            <a class="btn btn-primary" v-bind:href="'/' + theatre['theatre_id'] + '/create_show'">Create Show</a>
        </div>
        </div>
    </div>
    <div v-if="isadmin === 'True'">
        <a class="btn btn-primary" href="/create_theatre">Create Theatre</a>
    </div>
    </div>
    `,
    data () {
        return {
        theatre_info : [],
        isadmin : document.getElementById('isadmin').getAttribute('value'),
        cur_user_id : document.getElementById('user_id').getAttribute('value')
        }
    },
    methods : {
        delete_theatre : function(t_id){
            var result = confirm('are you sure about deleting this theatre and all of its corresponding shows?')
            if (result){
                fetch('http://127.0.0.1:8080/delete_theatre/'+t_id,{
                    method:"GET",
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authentication-Token' : localStorage.getItem('Authentication-Token')
                    }
                }).then((response) => {
                    return response.text()
                }).then((data) => {
                    alert(data);
                    location.replace('http://127.0.0.1:8080/')
                }).catch((err) => {
                    alert(err.message)
                })
            }
        },
        delete_show : function(t_id,s_id){
            var result = confirm('are you sure about deleting this show?')
            if (result){
                fetch('http://127.0.0.1:8080/'+t_id+'/delete_show/'+s_id,{
                    method:"GET",
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authentication-Token' : localStorage.getItem('Authentication-Token')
                    }
                }).then((response) => {
                    return response.text()
                }).then((data) => {
                    alert(data);
                    location.replace('http://127.0.0.1:8080/')
                }).catch((err) => {
                    alert(err.message)
                })
            }
        }
    },
    mounted : function() {
        fetch('http://127.0.0.1:8080/theatre_shows',{
        method : 'GET',
        headers : {
            'Content-Type' : 'application/json',
            'Authentication-Token' : localStorage.getItem('Authentication-Token')
        }
        }).then((response) =>{
            if(response.ok){
                return response.json()
            }else{
                fetch('http://127.0.0.1:8080/logout'
                ).then((response) => {
                    return response.text()
                }).then((data) => {
                    console.log(data);
                    location.replace('http://127.0.0.1:8080/login')
                })
            }
        }).then((data) =>{
            this.theatre_info=data
        }).catch((err) =>{
            alert(err.message)
        })
    }
})

Vue.component('login-page',{
    template : `
    <div>
    <div>
      <label>username: </label>
      <input type="text" name="username" v-model="logindata.username" required>
    </div>
    <div>
      <label> password: </label>
      <input type="password" name="password" v-model="logindata.password" required>
    </div>
    <div>
      <button v-on:click="login">Submit</button>
    </div>
    </div>
    `,
    data () {
      return {
        logindata : {
        username : '',
        password : ''
      }
    }
  },
    methods : {
      login(){
        console.log(this.logindata)
        fetch('http://127.0.0.1:8080/login?include_auth_token',{
          method :"POST",
          body : JSON.stringify(this.logindata),
          headers : {
            'Content-Type' : 'application/json',
          }
        }).then((response) => {
        return response.json()
        }).then((data) => {
          localStorage.setItem('Authentication-Token', data.response.user['authentication_token'])
          location.replace('http://127.0.0.1:8080/')
        }).catch((err) => {
          console.log(err.message)
          alert("invalid username or password")
        })
      }
    }
})

Vue.component("create_theatre",{
    template : `
    <div>
    <div>
        <label>Theatre name:</label>
        <input type="text" v-model="theatre_data.theatre_name" id="theatre_name" required>
    </div>
    <div>
        <label>Theatre place:</label>
        <input type="text" v-model="theatre_data.theatre_place" id="theatre_place" required>
    </div>
    <div>
        <label>Theatre location:</label>
        <input type="text" v-model="theatre_data.theatre_location" id="theatre_location" required>
    </div>
    <div>
        <label>Theatre capacity:</label>
        <input type="number" v-model="theatre_data.theatre_capacity" id="theatre_capacity" required>
    </div>
    <button v-on:click="confirm_create_theatre">Create Theatre</button>
    </div>
    `,
    data () {
    return {
        theatre_data : {
        theatre_name : "",
        theatre_place : "",
        theatre_location : "",
        theatre_capacity : 1
    }}},
    methods : {
        confirm_create_theatre : function(){
            fetch('http://127.0.0.1:8080/create_theatre',{
                method : "POST",
                body : JSON.stringify(this.theatre_data),
                headers : {
                    'Content-Type' : 'application/json',
                    'Authentication-Token' : localStorage.getItem('Authentication-Token')
                }
            }).then((response) => {
                return response.text()
            }).then((data) => {
                console.log(data);
                alert(data);
                location.replace('http://127.0.0.1:8080/')
            }).catch((err) => {
                console.log(theatre_data)
                console.log(err.message);
                alert("Something went wrong. Try again.")
            })
        }
    }
})

Vue.component('edit_theatre',{
    template : `
    <div>
    <div>
        <label>Theatre name:</label>
        <input type="text" v-model="theatre_data.theatre_name"  id="theatre_name" required>
    </div>
    <div>
        <label>Theatre place:</label>
        <input type="text" v-model="theatre_data.theatre_place" id="theatre_place" required>
    </div>
    <div>
        <label>Theatre location:</label>
        <input type="text" v-model="theatre_data.theatre_location" id="theatre_location" required>
    </div>
    <div>
        <label>Theatre capacity:</label>
        <input type="number" v-model="theatre_data.theatre_capacity" id="theatre_capacity"  required>
    </div>
    <button v-on:click="confirm_edit_theatre">confirm edit</button>
    </div>
    `,
    data () { 
    return {
    theatre_data : {
        theatre_name : "",
        theatre_place : "",
        theatre_location : "",
        theatre_capacity : 1
    }}},
    methods : {
        confirm_edit_theatre : function(){
            ///console.log(window.location.href);
            fetch(window.location.href,{
                method : "POST",
                body : JSON.stringify(this.theatre_data),
                headers : {
                    'Content-Type' : 'application/json',
                    'Authentication-Token' : localStorage.getItem('Authentication-Token')
                }
            }).then((response) => {
                return response.text()
            }).then((data) => {
                console.log(data);
                alert(data)
                location.replace('http://127.0.0.1:8080/')
            }).catch((err) => {
                alert("something went wrong.")
            })
        }
    }
})

Vue.component('create-show',{
    template : `
    <div>
    <div>
        <label>Show name:</label>
        <input type="text" v-model="show_data.show_name" id="show_name" required>
    </div>
    <div>
        <label>Show Timing:</label>
        <input type="time" v-model="show_data.show_timing" id="show_timing" required>
    </div>
    <div>
        <label>Show Tags:</label>
        <input type="text" v-model="show_data.show_tags" id="show_tags" required>
    </div>
    <div>
        <label>Ticket price:</label>
        <input type="number" v-model="show_data.price" id="price" required>
    </div>
    <button v-on:click="create_show">Create show</button>
    </div>
    `,
    data () {
        return {
        show_data:{
            show_name : "",
            show_timing : "",
            show_tags : "",
            price : 100
    }}},
    methods : {
        create_show : function(){
            fetch(window.location.href,{
                method : "POST",
                body : JSON.stringify(this.show_data),
                headers : {
                    'Content-Type' : 'application/json',
                    'Authentication-Token' : localStorage.getItem('Authentication-Token')
                }
            }).then((response) => {
                return response.text()
            }).then((data) => {
                console.log(data);
                alert(data);
                location.replace('http://127.0.0.1:8080/')
            }).catch((err) => {
                alert(err.message)
            })
        }
    }
})


Vue.component('edit-show',{
    template : `
    <div>
    <div>
        <label>Show name:</label>
        <input type="text" v-model="show_data.show_name" id="show_name" required>
    </div>
    <div>
        <label>Show Timing:</label>
        <input type="time" v-model="show_data.show_timing" id="show_timing" required>
    </div>
    <div>
        <label>Show Tags:</label>
        <input type="text" v-model="show_data.show_tags" id="show_tags" required>
    </div>
    <div>
        <label>Ticket price:</label>
        <input type="number" v-model="show_data.price" id="price" required>
    </div>
    <button v-on:click="edit_show">Edit Show</button>
    </div>
    `,
    data () {
        return {
        show_data :{
            show_name : "",
            show_timing : "",
            show_tags : "",
            price : 100
    }}},
    methods : {
        edit_show : function(){
            fetch(window.location.href,{
                method : "POST",
                body : JSON.stringify(this.show_data),
                headers : {
                    'Content-Type' : 'application/json',
                    'Authentication-Token' : localStorage.getItem('Authentication-Token')
                }
            }).then((response) => {
                return response.text()
            }).then((data) => {
                alert(data);
                location.replace('http://127.0.0.1:8080/')
            }).catch((err) =>{
                alert(err.message)
            })
        }
    }
})

Vue.component('book-show',{
    template : `
    {% raw %}
    <div>
        <p>Total Tickets : {{ total_tickets }}</p>
        <p>Tickets Available : {{ available_tickets }}</p>
        <div>
            <label>No of Tickets:</label>
            <input type="number" id="ticket_count"  v-model="ticket_count" min="1" max="available_tickets" step="1" required>
        </div>
        <div>
            <label>Price of a Ticket:</label>
            <input type="number"  id="ticket_price"  v-model="price_of_one_ticket"  readonly>
        </div>
        <div>
            <label>Total price:</label>
            <input type="number" id="cost" v-model="total_price" readonly>
        </div>
        <button v-on:click="confirm_booking">Book Show</button>
    </div>
    {% endraw %}
    `,
    data () {
        return {
        available_tickets: 0,
        total_tickets : 0,
        price_of_one_ticket : 0,
        ticket_count : 1,
        total_price : 0
    }},
    methods : {
        confirm_booking : function(){
            if (this.ticket_count <= this.available_tickets){
                fetch(window.location.href,{
                    method : "POST",
                    body : JSON.stringify(this.ticket_count),
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authentication-Token' : localStorage.getItem('Authentication-Token')
                    }
                }).then((response) => {
                    return response.text()
                }).then((data) => {
                    alert(data);
                    location.replace('http://127.0.0.1:8080/')
                }).catch((err) => {
                    alert(err);
                    location.replace('http://127.0.0.1:8080/')
                })
            }else{
                alert("select tickets within the range of available tickets.")
            }
    }
    },
    watch : {
        ticket_count(){
            this.total_price = this.ticket_count * this.price_of_one_ticket;
        }},
    mounted : function(){
        fetch(window.location.href,{
            method : "GET",
            headers : {
                'Content-Type' : 'application/json'
            }
        }).then((response) => {
            console.log(response.ok)
            if(response.ok){
                return response.json()
            }else{
                return response.text()
            }
        }).then((data) => {
            if (data == "HOUSEFULL"){
                console.log(data);
                alert(data);
                location.replace('http://127.0.0.1:8080/')
            }else{
                console.log(data.available_tickets);
                this.available_tickets=data.available_tickets;
                this.total_tickets=data.theatre_capacity;
                this.price_of_one_ticket=data.price;
                this.total_price=data.price
            }
        }).catch((err) => {
            alert(err);
        })
    }
})


Vue.component('user-bookings',{
    template : `
    {% raw %}
    <div v-if="bookings_data.length === 0">
        <p>No Bookings of the current user has been found.</p>
    </div>
    <div v-else>
        <div v-for="b in bookings_data">
            <div class="container border">
            <h3>{{b['show_details']['show_name']}}</h3>
            <p>Movie Genre:{{b['show_details']['show_tags']}}</p>
            <p>Theatre name:{{b['show_details']['theatre_name']}}
            <p>Tickets booked:{{b['tickets_booked']}}</p>
            <p>booked on: {{b['booked_time']}}</p>
            </div>
        </div>
    </div>
    {% endraw %}`,
    data () {
        return {
        bookings_data : []
    }},
    mounted : function(){
        console.log(this.user_id)
        fetch(window.location.href ,{
            method : 'GET',
            headers : {
                'Content-Type' : 'application/json'
            }}).then((response) => {
                return response.json()
            }).then((data) => {
                console.log(data)
                this.bookings_data=data
            }).catch((err) => {
                alert(err.message)
            })
}})

Vue.component('search_display',{
    template : `
    <div>
    <div>
    <div>
    <label>Search for:</label>
    <input type="text" name="search_term" v-model="search_term">
    </div>
    <div>
      <input type="radio" name="search_in" value="theatre_name" v-model="search_in" checked> <label>Theatre Name</label>
      <input type="radio" name="search_in" value="theatre_location" v-model="search_in"> <label>Theatre location</label>
      <input type="radio" name="search_in" value="show_name" v-model="search_in"> <label>Show Name</label>
      <input type="radio" name="search_in" value="show_tags" v-model="search_in"> <label>Show Tags</label>
    </div>
  </div>
  <button v-on:click="search"> Search</button>
  <div>
 
  <div>
  <div v-if="this.search_results.length === 0 ">No Results found.</div>
  <div v-else>
    <div v-if="this.search_in === 'theatre_name'">
      <div v-for="t in this.search_results">
      <div class="border">
        <p>{{t['theatre_name']}}</p>
        <div class="border" v-for="s in t['shows']">
          <p>{{s['show_name']}}</p>
          <p>{{s['show_timing']}}</p>
          <p>{{s['show_start_timing']}}</p>
          <a class="btn btn-outline-danger" v-bind:href="'/book_show/'+ cur_user_id + '/' + s['show_id']">Book show</a>
        </div>
      </div>  
      </div>
    </div>
    <div v-else-if="this.search_in === 'theatre_location'">
      <div v-for="t in this.search_results">
      <div class="border">
        <h3>{{t['theatre_name']}}</h3>
        <p>{{t['theatre_location']}}</p>
        <div class="border" v-for="s in t['shows']">
          <p>{{s['show_name']}}</p>
          <p>{{s['show_timing']}}</p>
          <p>{{s['show_start_timing']}}</p>
          <a class="btn btn-outline-danger" v-bind:href="'/book_show/'+ cur_user_id + '/' + s['show_id']">Book show</a>
        </div>
      </div>
      </div>
    </div>
    <div v-else-if="this.search_in === 'show_name'">
      <div v-for="s in this.search_results">
        <div class="border">
          <p>{{s['show_name']}}</p>
          <p>{{s['show_timing']}}</p>
          <p>{{s['show_start_timing']}}</p>
          <p>{{s['show_tags']}}</p>
          <a class="btn btn-outline-danger" v-bind:href="'/book_show/'+ cur_user_id + '/' + s['show_id']">Book show</a>
        </div>
      </div>
    </div>
    <div v-else-if="this.search_in === 'show_tags'">
      <div v-for="s in this.search_results">
        <div class="border">
          <p>{{s['show_name']}}</p>
          <p>{{s['show_timing']}}</p>
          <p>{{s['show_start_timing']}}</p>
          <p>{{s['show_tags']}}</p>
          <a class="btn btn-outline-danger" v-bind:href="'/book_show/'+ cur_user_id + '/' + s['show_id']">Book show</a>
        </div>
      </div>
    </div>
  </div>
  </div>
  </div>
  
  </div>
    `,
    data () { 
      return {
      search_term : '',
      search_in : '',
      search_results : [],
      cur_user_id : document.getElementById('user_id').getAttribute('value')
    }},
    methods : {
      search(){
        search_data = {"search_term" : this.search_term, "search_in" : this.search_in}
        console.log(search_data)
        fetch('http://127.0.0.1:8080/search',{
          method : 'POST',
          body : JSON.stringify(search_data),
          headers : {
            'Content-Type' : 'application/json',
            'Authentication-Token' : localStorage.getItem('Authentication-Token')
          }
        }).then((response) => {
          return response.json()
        }).then((data) => {
          console.log(data)
          this.search_results=data
        }).catch((err) => {
        alert(err.message)
      })
      }
    }
})


Vue.component('logout-btn',{
    template : `
    <div style="text-align:right;">
        <button v-on:click="logout_fn">logout</button>
    </div>
    `,
    methods : {
        logout_fn(){
            localStorage.removeItem('Authentication-Token')
            fetch('http://127.0.0.1:8080/logout'
            ).then((response) => {
                return response.text()
            }).then((data) => {
                console.log(data);
                location.replace('http://127.0.0.1:8080/login')
            })
        }
    }
})


function logout_user(){
    localStorage.removeItem('Authentication-Token')
    fetch('http://127.0.0.1:8080/logout',{
        method : 'GET'
    }).then((response) => {
        return response.text()
    }).then((data) => {
        alert(data)
    })
}

var app = new Vue({
    el : "#app"
})