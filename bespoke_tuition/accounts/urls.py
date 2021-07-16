from django.urls import path

from . import views

'''app_name = 'accounts'
urlpatterns = [
    path('', views.home),
    path('yourinfo/', views.client),
    path('yourchild/', views.child),
    path('youraccounts/', views.accounts),
    path('youraccounts/invoices', views.invoices),
]'''

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('allclients/', views.allClients, name='allclients'),
    path('allclients/addnewclient', views.addClient, name='addclient'),
    path('allstudents/', views.allStudents, name='allstudents'),
    path('allstudents/addnewstudent', views.addStudent, name='addstudent'),
    path('products&terms', views.referenceData, name='refdata'),
    path('products&terms/addnewproduct', views.addProducts, name='addproduct'),
    path('products&terms/addnewproduct/<int:product>', views.updateProduct, name='updateproduct'),
    path('products&terms/addnewterm', views.addTerms, name='addterm'),
    path('products&terms/addnewterm/<int:term>', views.updateTerm, name='updateterm'),
    path('yourinformation', views.clientView, name='clientview'),
    path('yourinvoices/', views.clientInvoices, name='clientinvoices'),
    path('yourinvoices/<int:invoice>', views.clientDetailedInvoice, name='clientdetailedinvoice'),
    path('yourinfo/<int:customer>', views.client, name='client'),
    path('yourchild/<int:student>', views.student, name='student'),
    path('yourchild/<int:student>/addlessons', views.addLessons, name='addlessons'),
    path('yourchild/<int:lesson>/updatelesson', views.updateLesson, name='updatelesson'),
    path('yourchild/<int:lesson>/deletelesson', views.deleteLesson, name='deletelesson'),
    path('createinvoices/', views.accounts, name='accounts'),
    path('createinvoices/<int:customer>', views.accountsDetailed, name='accountsdetailed'),
    path('invoices/', views.invoices, name='invoices'),
    path('invoices/<int:invoice>', views.invoicesDetailed, name='invoicesdetailed'),
    path('invoices/<int:invoice>/update', views.updateInvoices, name='updateinvoice'),
]

#app_name = 'polls'
#urlpatterns = [
#    path('', views.IndexView.as_view(), name='index'),
#    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#    path('<int:question_id>/vote/', views.vote, name='vote'),
#]