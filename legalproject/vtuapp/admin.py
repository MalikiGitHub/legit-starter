from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
    
    list_display =['username',"FullName",'email','user_type','Phone','Account_Balance','referer_username','referals','Referer_Bonus','id','last_login','date_joined','verify']
    search_fields = ('username','email','Phone','referer_username','id','user_type')

    def referals(self, obj):
        a = CustomUser.objects.get(id = obj.id)
        return Referal_list.objects.filter(user=a).count()

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('user_type','reservedaccountNumber','verify','email_verify')}),
             ("Profile", {'fields': ('image_tag',"FullName",'Phone',"Account_Balance",'referer_username','Referer_Bonus',"BVN","DOB",'BankName','AccountNumber','AccountName',"Gender","State_of_origin","Local_gov_of_origin")}),
    )

    readonly_fields = ('image_tag','FullName','Address',"Account_Balance", 'referer_username','Referer_Bonus','BankName','AccountNumber','AccountName',"BVN","DOB","Gender","State_of_origin","Local_gov_of_origin", )



admin.site.register(CustomUser,CustomUserAdmin)