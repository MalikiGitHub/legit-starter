from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
    
    list_display =['username',"first_name", 'last_name', 'email','user_type','Phone','Account_Balance','referer_username','referals','Referer_Bonus','id','last_login','date_joined','verify']
    search_fields = ('username','email','Phone','referer_username','id','user_type')

    def referals(self, obj):
        a = CustomUser.objects.get(id = obj.id)
        return Referal_list.objects.filter(user=a).count()

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('user_type','reservedaccountNumber','verify','email_verify')}),
            #  ("Profile", {'fields': ('image_tag', "first_name",'last_name', 'Phone',"Account_Balance",'referer_username','Referer_Bonus',"BVN","DOB",'BankName','AccountNumber','AccountName',"Gender","State_of_origin","Local_gov_of_origin")}),
    )

    readonly_fields = ('first_name', 'last_name', 'Address',"Account_Balance", 'referer_username','Referer_Bonus', 'email', )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'dob', 'profile_image', 'account_name', 'account_number', 'gender', 'state_of_origin', 'local_gov_of_origin']
    readonly_fields = ['user', 'dob', 'gender']
    

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(WebsiteConfiguration)