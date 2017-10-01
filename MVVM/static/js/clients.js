$(document).ready(function(){

    function Client(data){
      var self = this
      self.title = ko.observable(data.title)
      self.description = ko.observable(data.description)
      self.client = ko.observable(data.client)
      self.priority = ko.observable(data.priority)
      self.due = ko.observable(data.due)
      self.productArea = ko.observable(data.productArea)
    }

    function ClientViewModel(){
      var self = this
      self.clientList = ko.observableArray([])
      self.clientListLoaded = false   

      self.loadClientList = function(){
        if(!self.clientListLoaded){
          $.getJSON("/clients", function(data){
              data.forEach(function(clientName){
                self.clientList.push(clientName)
            })           
          })  
          self.clientListLoaded = true;        
        }
      }   
    }

    $(function(){
      cvm = new ClientViewModel()
      ko.applyBindings(cvm)
      cvm.loadClientList()
    });
})