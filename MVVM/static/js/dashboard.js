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
      
    }

    $(function(){
      fvm = new FeatureViewModel()
      ko.applyBindings(fvm)
      fvm.loadClientList()
    });
})