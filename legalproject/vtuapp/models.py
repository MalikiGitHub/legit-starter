
import json
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator
from django.db import transaction
from django.conf import settings

# Create your models here.


User = settings.AUTH_USER_MODEL

Bank = (
    ('Access Bank', 'Access Bank'),
    ('Access(Diamond) Bank', 'Access (Diamond) Bank'),
    ('ECO Bank', 'ECO Bank'),
    ('First Bank of Nigeria', 'First Bank of Nigeria'),
    ('FCMBank', 'FCMBank'),
    ('FIdelity Bank', 'FIdelity Bank'),
    ('GTBank', 'GTBank'),
    ('Heritage Bank', 'Heritage Bank'),
    ('Kuda Bank', 'Kuda Bank'),
    ('Opay', 'Opay'),
    ('Palmpay', 'Palmpay'),
    ('Polarise Bank', 'Polarise Bank'),
    ('Stanbic IBTC', 'Stanbic IBTC'),
    ('Sterling Bank', 'Sterling Bank'),
    ('UBA', 'UBA'),
    ('Union Bank', 'Union Bank'),
    ('Unity Bank', 'Unity Bank'),
    ('Wema Bank', 'Wema Bank'),
    ('Zenith Bank', 'Zenith Bank'),
)


user_t = (
    ("Smart Earner", "Smart Earner"),
    ("Affilliate", "Affilliate"),
    ("TopUser", "TopUser"),
    ("API", "API")
)

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField()
    first_name = models.CharField(max_length=200,  null=True)
    last_name = models.CharField(max_length=200,  null=True)
    Address = models.CharField(max_length=500,  null=True)
    BankName = models.CharField(max_length=100, choices=Bank, blank=True)
    AccountNumber = models.CharField(max_length=40, blank=True)
    Phone = models.CharField(max_length=14, blank=True)
    AccountName = models.CharField(max_length=200, blank=True)
    Account_Balance = models.FloatField(default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    pin = models.CharField(null=True, blank=True, max_length=5)
    referer_username = models.CharField(max_length=50, blank=True, null=True)
    first_payment = models.BooleanField(default=False)
    Referer_Bonus = models.FloatField(default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    user_type = models.CharField(max_length=30, choices=user_t, default="Smart Earner", null=True)
    reservedaccountNumber = models.CharField(max_length=100, blank=True, null=True)
    reservedbankName = models.CharField(max_length=100, blank=True, null=True)
    reservedaccountReference = models.CharField(max_length=100, blank=True, null=True)
    Bonus = models.FloatField(default=0.00, null=True, validators=[ MinValueValidator(0.0)],)
    verify = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=False)
    

    def f_account(self):
        try:
            return json.loads(self.accounts)
        except:
            return {"accounts":[] }
    
    def passport(self):
       
        if self.passport_photogragh:
            return "https://www.legitdata.com.ngmedia/%s" % (self.passport_photogragh)
        else:
            return "https://png.pngtree.com/png-vector/20190704/ourmid/pngtree-businessman-user-avatar-free-vector-png-image_1538405.jpg"


    def __str__(self):
        return self.username

    def image_tag(self):
        
        from django.utils.html import mark_safe
        return mark_safe('<img src="https://www.legitdata.com.ngmedia/%s" width="150" height="150" />' % (self.passport_photogragh))

    image_tag.short_description = 'Image'

    def walletb(self):
         return  str(round(self.Account_Balance))

    def bonusb(self):
         return  str(round(self.Referer_Bonus))

    def ref_deposit(self, amount):
        self.Referer_Bonus += amount
        self.Referer_Bonus = round(self.Referer_Bonus, 2)
        self.save()
       

    def ref_withdraw(self, amount):
        if self.self.Referer_Bonus > amount or amount < 0 :
            return False
        self.Referer_Bonus -= amount
        self.Referer_Bonus = round(self.Referer_Bonus, 2)
        self.save()
        

    # @classmethod
    # def withdraw(cls, id, amount):
    #     with transaction.atomic():
    #         account = (cls.objects.select_for_update().get(id=id))
    #         #print(account)
    #         balance_before = account.Account_Balance
    #         if account.Account_Balance < amount or amount < 0:
    #             return False
    #         account.Account_Balance -= amount
    #         account.save()

    #     try:

    #         Transactions.objects.create(user=CustomUser.objects.get(id=id),
    #             transaction_type="DEBIT", balance_before= balance_before,balance_after = balance_before -amount,amount=amount)

    #     except:
    #         pass

    # @classmethod
    # def deposit(cls, id, amount, transfer=False,medium = "NONE" ):
    #     with transaction.atomic():
    #         account = (cls.objects.select_for_update().get(id=id))
            # if transfer == False:
            #     if account.referer_username:
            #         if CustomUser.objects.filter(username__iexact=account.referer_username).exists():
            #             if account.first_payment == False:
            #                 referer = CustomUser.objects.get(
            #                     username__iexact=account.referer_username)
            #                 if amount >= 5000:
            #                     referer.ref_deposit(100)
            #                     account.first_payment = True
            #                 else:
            #                     referer.ref_deposit((0.05*amount))
            #                     account.first_payment = True

        #     balance_before = account.Account_Balance
        #     if medium != "NONE" : 

        #             if Charge_user.objects.filter(username = account.username).exists():
        #                     pending_charge = Charge_user.objects.filter(username =account.username).last()
        #                     if pending_charge.pending_amount > 0:
        #                             if amount > pending_charge.pending_amount:
        #                                 amt = amount - pending_charge.pending_amount
        #                                 balance_before = account.Account_Balance
        #                                 pending_charge.balance_before = balance_before
        #                                 account.Account_Balance += amt
        #                                 account.save()

        #                                 try:
        #                                     Wallet_summary.objects.create(user=account, product=f"N{pending_charge.pending_amount} pending wallet charge paid", amount=amount, previous_balance = balance_before, after_balance= balance_before + amount)
        #                                 except:
        #                                     pass
        #                                 pending_charge.comment = f"N{pending_charge.pending_amount} pending wallet charge paid"
        #                                 pending_charge.balance_after = amt
        #                                 pending_charge.pending_amount = 0
        #                                 pending_charge.save()


                                        


        #                             else:
        #                                 balance_before = account.Account_Balance
        #                                 pending_charge.balance_before = balance_before
        #                                 amt = pending_charge.pending_amount - amount 
        #                                 pending_charge.comment = f"N{amount} paid from  pending wallet charge, pending amount remain {amount} "
        #                                 pending_charge.pending_amount =  amt
        #                                 pending_charge.balance_after = 0
        #                                 pending_charge.save()


                                          
        #                     else: 
        #                           account.Account_Balance += amount
        #                           account.save()
        #             else:
        #                   account.Account_Balance += amount
        #                   account.save()
                    
        #     try:

        #         Transactions.objects.create(user=CustomUser.objects.get(id=id),
        #             transaction_type="CREDIT",balance_before= balance_before,balance_after = balance_before + amount, amount= amount)

        #     except:
        #         pass

        #     try:
        #          Wallet_Funding.objects.create(user=CustomUser.objects.get(id=id),medium=medium,previous_balance= balance_before,after_balance= balance_before + amount, amount= amount)

        #     except:
        #             pass


        # return account 
        
        
class Referal_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    username = models.CharField(max_length=30)
    referal_user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="referal")
    create_date = models.DateTimeField(default=timezone.now,editable=False)

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        mb = CustomUser.objects.get(username__iexact=self.username)
        self.referal_user = mb

        super(Referal_list, self).save(*args, **kwargs)
        
        
        
        
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(default='default.jpg', upload_to="profile_pics", blank=True)
    account_name = models.CharField(max_length=30, null=True, blank=True)
    account_number = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=6, null=True,)
    state_of_origin = models.CharField(max_length=100, null=True,)
    local_gov_of_origin = models.CharField(max_length=100, null=True, blank=True)
    BVN = models.CharField(max_length=50, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.user}'s Profile"
    
    
    
    
    
class WebsiteConfiguration(models.Model):
    primary_color = ColorField(default='#132563')
    secondary_color = ColorField(null=True, blank=True, help_text="add this color if you want to use color mixure or gradient else leave blank to use single color")
    intro_message = models.TextField(default="Refer people to legitdata and earn N500 immediately the person upgrade his/her account to affiliate or topuser",null=True, blank=True)
    sms_notification_number = models.CharField(max_length=500, null=True, blank=True,help_text="Enter the phone number to recieve SMS notifications on")
    support_phone_number = models.CharField(max_length=13, null=True, blank=True, help_text="Customer support phone number ,Whatsapp number  (start with 234)")
    whatsapp_group_link = models.URLField(null=True, blank=True, help_text="Support group link if any")
    gmail = models.EmailField( null=True, blank=True, help_text="Email to get notification on")
    
    ######## PAYMENT GATEWAYS
    manual_bank_funding_limit =  models.PositiveIntegerField(default=5000, help_text="minimum amount allowed for FUND WITH MANUAL BANK TRANSFER")
    manual_bank_funding_info_message = models.TextField(default="Your account will be suspended if you submit without transfer \n Please note that there is a charge of N50 if the amount greater than N9,999.",null=True, blank=True)
    Paystack_secret_key = models.CharField(max_length=500, null=True, blank=True,help_text="Enter your Paystack SCRET API KEY here if you are using Paystack, else leave blank")
    monnify_API_KEY = models.CharField(max_length=500, null=True, blank=True,help_text="Enter your monnify  API_KEY here if you are using monnify  else leave blank")
    monnify_SECRET_KEY = models.CharField(max_length=500, null=True, blank=True,help_text="Enter your monnify Secret Key here if you are using monnify else leave blank")
    monnify_contract_code = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your monnify contarct code here if you are using monnify else leave blank")
    
    ########### API/AUTOMATION
    ringo_email = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your RINGO Email here if you are using VTpass else leave blank")
    ringo_password = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your RINGO password here if you are using VTpass else leave blank")
    
    vtpass_email = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your Vtpass Email here if you are using VTpass else leave blank")
    vtpass_password = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your Vtpass password here if you are using VTpass else leave blank")
    
    hollatag_username = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your hollatag username here if you are using hollatag else leave blank")
    hollatag_password = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your hollatag  password here if you are using hollatag else leave blank")
                                         
    sme_plug_secret_key = models.CharField(max_length=500, null=True, blank=True,help_text="Enter your SMEPLUG SCRET API KEY here if you are using SMEplug else leave blank")
    
    simhost_API_key = models.CharField(max_length=500, null=True, blank=True,help_text="Enter your simhost APIKEY here if you are using simhost else leave blank")
    
    msplug_API_key = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your msplug APIKEY here if you are using msplug else leave blank")
    
    vtu_auto_email = models.CharField(max_length=500, null=True, blank=True,help_text="Enter your vtuauto Email here if you are using vtuauto else leave blank")
    vtu_auto_password = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your vtuauto Password here if you are using vtuauto else leave blank")
    
    mobilenig_username = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your mobilenig username here if you are using mobilenig else leave blank")
    mobilenig_api_key = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your mobilenig APIKEY here if you are using mobilenig else leave blank")
    idchecker_api_key = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your idchecker APIKEY here if you are using idchecker else leave blank")
    uws_token = models.TextField( null=True, blank=True,)
    qtopup_api_key = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your qtopup APIKEY here if you are using qtopup else leave blank")
    
    ########## MSORD WEB API
    msorg_web_url = models.URLField( null=True, blank=True,)
    msorg_web_api_key = models.TextField(max_length=500, null=True, blank=True, help_text="Enter your MSORG website APIKEY here if you are using website developed by MSORG else leave blank")
    msorg_web_url_2  = models.URLField( null=True, blank=True,)
    msorg_web_api_key_2  = models.TextField(max_length=500, null=True, blank=True, help_text="Enter your APIKEY for your 2nd MSORG WEBSITE here if you are using website developed by MSORG else leave blank")
    msorg_web_url_3 = models.URLField( null=True, blank=True,)
    msorg_web_api_key_3 = models.TextField(max_length=500, null=True, blank=True, help_text="Enter your APIKEY for your 3rd choice MSORG WEBSITE here if you are using website developed by MSORG else leave blank")
    
    ############## ACCOUNT UPGRADE
    affiliate_upgrade_fee = models.IntegerField(default=2000,blank=True, null=True, verbose_name="Upgrade to Affiliate charge")
    affiliate_to_topuser_upgrade_fee = models.IntegerField(default=3000,blank=True, null=True,verbose_name="Upgrade from Affiliate to TopUser charge")
    topuser_upgrade_fee = models.IntegerField(default=5000,blank=True, null=True, verbose_name="Upgrade to TopUser charge")
    
    ############## REFERRAL BONUS
    affiliate_referral_bonus = models.IntegerField(default=500,blank=True, null=True, help_text="set amount upline/referee earns when downline/referral upgrades to Affiliate package")
    affiliate_to_topuser_referral_bonus = models.IntegerField(default=500,blank=True, null=True, help_text="set amount upline/referee earns when downline/referral upgrades from Affiliate to TopUser package")
    topuser_referral_bonus = models.IntegerField(default=1000,blank=True, null=True, help_text="set amount upline/referee earns when downline/referral upgrades to TopUser package")
    
    ############## CONTROLLER
    ResultCheckerSource = models.CharField(max_length=50, blank=True, null=True, default="API", choices=( ('API','API'),('MANUAL','MANUAL'), ))
    Cable_provider = models.CharField(max_length=50, blank=True, null=True, default="VTPASS", choices=( ('VTPASS','VTPASS'),('RINGO','RINGO'), ))
    Bill_provider = models.CharField(max_length=50, blank=True, null=True, default="VTPASS", choices=( ('VTPASS','VTPASS'),('RINGO','RINGO'), ))
    disable_Transaction_limit = models.BooleanField(max_length=50, default=False, choices=( (True,'YES'),(False,'NO'), ), verbose_name="Disable Transaction limit for unverified user")

    ############## UNVERIFIED USER LIMITS
    # unverified_users_data_TopUp_limit =  models.PositiveIntegerField(default=10000, help_text="maximum amount of data TopUp allowed for unverified users DAILY")
    # unverified_users_airtime_TopUp_limit =  models.PositiveIntegerField(default=10000, help_text="maximum amount of Airtime TopUp allowed for unverified users DAILY")
    unverified_users_daily_withdraws_limit =  models.PositiveIntegerField(default=5000, help_text="maximum amount of withdrawal allowed for unverified users DAILY")
    unverified_users_transfer_limit =  models.PositiveIntegerField(default=5000, help_text="total amount of transfer allowed for unverified users DAILY")
    unverified_users_daily_transation_limit =  models.PositiveIntegerField(default=30000, help_text="total amount of transaction allowed for unverified users DAILY")


    def save(self, *args, **kwargs):
        if WebsiteConfiguration.objects.all():
            WebsiteConfiguration.objects.all().delete()

        super(WebsiteConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        return "Website Configuration"

    class Meta:
        verbose_name_plural = 'WEBSITE CONFIGURATIONS'
        
config = ''
config = WebsiteConfiguration.objects.all().first()