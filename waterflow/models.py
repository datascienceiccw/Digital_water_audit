from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from computedfields.models import ComputedFieldsModel, computed, compute


reject_to_choices = [
  ('1','ETP'),
  ('2','STP'),
  ('3','Municipal Line')
]

class Registration(models.Model):
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    company_name = models.TextField(null=False)
    designation = models.TextField(null=True)
    email = models.EmailField(null=False)
    mobile_number = models.TextField(null=False)

class BasicDetails(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    designation = models.TextField(null=True)
    contact_number = models.TextField(null=False)
    email_address = models.EmailField(null=False)
    organization_name = models.TextField(null=False)
    organization_web_address = models.TextField(null=True)
    address = models.TextField(null=True)
    organization_type = models.TextField(null=True,blank=True,default='Hospitality')
    num_permanent_employees = models.IntegerField(default=0)
    num_temporary_employees = models.IntegerField(default=0)
    num_rooms = models.IntegerField(default=0)
    average_occupancy = models.IntegerField(default=0, help_text='Average number of rooms occupied in an year.')
    average_room_occupancy = models.IntegerField(default=0, help_text='Average number of people per room.')
    total_area = models.IntegerField(default=0)
    total_built_up_area = models.IntegerField(default=0)
    total_green_area = models.IntegerField(default=0)
    total_air_conditioned_space_area = models.IntegerField(default=0)
    pin_code = models.IntegerField()


class SourceWaterProfile(models.Model):
    SOURCE_CHOICES = [
        ('Borewell Water', 'Borewell Water'),
        ('Tanker water', 'Tanker water'),
        ('Metro/corporation Water', 'Metro/corporation Water'),
        ('Rainwater', 'Rainwater'),
        ('Others', 'Others'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source_name = models.CharField(max_length=255, choices=SOURCE_CHOICES)
    source_daily_consumption = models.FloatField(null=True, blank=True)
    source_water_cost = models.FloatField(null=True, blank=True)
    
    def get_source_name_display(self):
        return dict(self.SOURCE_CHOICES).get(self.source_name, "Unknown")

  


class RainWaterProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  amount_harvested_water_last_two_years = models.FloatField(default=0)
  amount_recharged_water_last_two_years = models.FloatField(default=0)
  rooftop_area = models.FloatField(default=0)
  paved_area = models.FloatField(default=0)
  unpaved_area = models.FloatField(default=0)

class FreshWaterTreatmentMethods(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class FreshWaterTreatmentProfile(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    # name = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)

    def get_method_name_display(self):
        return [method.name for method in self.name.all()]

class OtherFreshwaterTreatmentMethods(models.Model):
    treatment_method = models.ForeignKey(FreshWaterTreatmentProfile, on_delete=models.CASCADE, related_name='other_treatment_method') 
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name   

class FreshWaterTreatmentProfileDetails(models.Model):
    profile = models.OneToOneField(
        FreshWaterTreatmentProfile, on_delete=models.CASCADE, related_name='details')
    input_water = models.DecimalField(max_digits=10, decimal_places=2)
    product_water = models.DecimalField(max_digits=10, decimal_places=2)
    reject_water = models.DecimalField(max_digits=10, decimal_places=2)
    reject_to = models.CharField(choices=reject_to_choices, max_length=255)
    backwash_time = models.IntegerField(null=True, blank=True)  # in mins/day
    rinse_time = models.IntegerField(null=True, blank=True)  # in mins/day
    flush_time = models.IntegerField(null=True, blank=True)  # in mins/day
    regeneration_time = models.IntegerField(null=True, blank=True)  # in mins/day
    frequency_of_backwash_and_rinse = models.IntegerField(null=True, blank=True)
    frequency_of_regeneration = models.IntegerField(null=True, blank=True)
    amount_of_water_for_brine_solution = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    recovery_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    def clean(self):
        if not self.input_water or not self.product_water:
            raise ValidationError("Input water and product water must be provided.")
        self.recovery_percentage = (self.product_water / self.input_water) * 100

class TanksCapacitiesSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class TanksCapacities(models.Model):
# The source can be kept as a sum of selected options in source water and freshwater treatment. This can be done in
# the view function. 
    tank_names = [('Input freshwater tank','Input freshwater tank'),
                ('Fire tank','Fire tank'),
                ('Softener Storage tank','Softener Storage tank'),
                ('RO Storage tank','RO Storage tank'),
                ('Flush tank','Flush tank'),
                ('Domestic Water tank','Domestic Water tank'),
                ('RO Input tank','RO Input tank'),
                ('Boiler Makeup tank','Boiler Makeup tank'),
                ('Others', 'Others')]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # For each name and capacity, add multiple choices using the add more button.
    # name = models.CharField(choices=tank_names,max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255, null=True, choices=tank_names)
    capacity = models.FloatField()
    def get_tank_name_display(self):
        return ', '.join(source.name for source in self.name.all())
    

class OtherTanksCapacitiesSource(models.Model):
    tanks_capacities = models.ForeignKey(TanksCapacities, on_delete=models.CASCADE, related_name='other_tank_source')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name    
    
class SourceWaterFlow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source = models.CharField(max_length=255,null=True,blank=True)
    destination = models.CharField(max_length=255,null=True,blank=True)


class DrinkingWaterSystem(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class DrinkingWaterSourceName(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name    


class DrinkingWaterSource(models.Model):
    used_by_choices = [
            ('1', 'Guest'),
            ('2', 'Employees'),
        ]
    source_name_choices = [
            ('In House RO System', 'In House RO System'),
            ('Bottled Water', 'Bottled Water'),
        ]
    source_choices = [
        ('1','Input freshwater tank'),
        ('2','Fire tank'),
        ('3','Softener Storage tank'),
        ('4','RO Storage tank'),
        ('5','Flush tank'),
        ('6','Domestic Water tank'),
        ('7','RO Input tank'),
        ('8','Boiler Makeup tank')
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # source_name = models.CharField(max_length=255, choices=source_name_choices)
    source_name = models.ManyToManyField(DrinkingWaterSystem, related_name='drinking_water_system')
    # other_source_name = models.CharField(max_length=255, null=True)
    source = models.ManyToManyField(DrinkingWaterSourceName, related_name='drinking_water_source', null=True)
    consumption = models.FloatField()
    cost = models.FloatField()
    used_by = models.CharField(max_length=255, choices=used_by_choices, null=True)  


class OtherDrinkingWaterSystem(models.Model):
    drinking_water_system = models.ForeignKey(DrinkingWaterSource, on_delete=models.CASCADE, related_name='other_water_system') 
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class OtherDrinkingWaterSourceName(models.Model):
    drinking_water_source = models.ForeignKey(DrinkingWaterSource, on_delete=models.CASCADE, related_name='other_drinking_source') 
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name   


class KitchenDishwasherTapConsumption(ComputedFieldsModel):
    kitchen_types = [
        ('1', 'Employee kitchen'),
        ('2', 'Guest kitchen'),
    ]
    reject_to_choices = [
    ('1','ETP'),
    ('2','STP'),
    ('3','Municipal Line')
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    kitchen_type = models.CharField(choices=kitchen_types, null=True, max_length=50)
    average_customers_per_day = models.IntegerField(null=True, blank=True)
    volume_consumed = models.FloatField(null=True, blank=True)
    cleaning = models.FloatField(null=True, blank=True)
    reject_to = models.CharField(max_length=50, choices=reject_to_choices, null=True)
    reject_volume =  models.FloatField(null=True, blank=True)
    dishwasher_loads = models.PositiveIntegerField(null=True, blank=True)
    consumption_per_load = models.FloatField(null=True, blank=True)
    handwash_tap_flowrate = models.FloatField(null=True, blank=True)
    handwash_tap_runtime = models.FloatField(null=True, blank=True)
    cleaning_tap_flowrate = models.FloatField(null=True, blank=True)
    cleaning_tap_runtime = models.FloatField(null=True, blank=True)

    @computed(models.FloatField())
    def cooking(self):
        return self.volume_consumed-self.cleaning
    @computed(models.FloatField())
    def dishwasher_total_consumption(self):
        return self.dishwasher_loads*self.consumption_per_load
    @computed(models.FloatField())
    def handwash_tap_consumption(self):
        return self.handwash_tap_flowrate*self.handwash_tap_runtime
    @computed(models.FloatField())
    def cleaning_tap_consumption(self):
        return self.cleaning_tap_flowrate*self.cleaning_tap_runtime

    def get_kitchen_type_display(self):
        return dict(self.kitchen_types).get(self.kitchen_type, "Unknown")

    def get_reject_to_display(self):
        return dict(self.reject_to_choices).get(self.reject_to, "Unknown")


class RestaurantConsumption(ComputedFieldsModel):
    accessible_choices = [
        ('1', 'Yes'),
        ('2', 'No'),
    ]
    reject_to_choices = [
    ('1','ETP'),
    ('2','STP'),
    ('3','Municipal Line')
    ]
    source_choices = [
        ('1','Input freshwater tank'),
        ('2','Fire tank'),
        ('3','Softener Storage tank'),
        ('4','RO Storage tank'),
        ('5','Flush tank'),
        ('6','Domestic Water tank'),
        ('7','RO Input tank'),
        ('8','Boiler Makeup tank'),
        ('9','Others')
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    restaurant_name = models.CharField(null=True, max_length=50) 
    accessible = models.CharField(choices = accessible_choices, null=True, max_length=50)
    average_occupancy = models.IntegerField(null=True, blank=True)
    reject_to = models.CharField(max_length=50, choices=reject_to_choices, null=True)
    tap_flowrate = models.FloatField(null=True, blank=True)
    
    # - compute field handwash water used volume = average occupancy in restauntants *2 handwash_tap_flowrate
    @computed(models.FloatField())
    def handwash_water_used_volume(self):
        return self.average_occupancy*2*self.tap_flowrate
    
    

    def get_reject_to_display(self):
        return dict(self.reject_to_choices).get(self.reject_to, "Unknown")  
    
class BanquetSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BanquetConsumption(ComputedFieldsModel):
    source_choices = [
        ('1','Input freshwater tank'),
        ('2','Fire tank'),
        ('3','Softener Storage tank'),
        ('4','RO Storage tank'),
        ('5','Flush tank'),
        ('6','Domestic Water tank'),
        ('7','RO Input tank'),
        ('8','Boiler Makeup tank'),
        ('9','Others')
    ]

    drinking_water_sources = [
            ('In House RO System', 'In House RO System'),
            ('Bottled Water', 'Bottled Water'),
            ('Individual RO Purifiers', 'Individual RO Purifiers'),
        ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    banquet_name = models.CharField(max_length=255)
    seating_capacity = models.IntegerField()
    average_occupancy = models.IntegerField()
    # drinking_water_source = models.CharField(choices=drinking_water_sources,null=True,max_length=100)
    drinking_water_source = models.ManyToManyField(BanquetSource, related_name='banquet')
    drinking_water_consumed = models.FloatField()
    tap_flowrate = models.FloatField()
    @computed(models.FloatField())
    def restroom_consumption(self):
        return self.average_occupancy*self.tap_flowrate*2
    

class OtherBanquetSource(models.Model):
    banquet_consumption = models.ForeignKey(BanquetConsumption, on_delete=models.CASCADE, related_name='other_banquet_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        

class GuestRoomDomesticSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name  

class GuestRoomToiletSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name               


class GuestRoomConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    types_of_commodes = [
        ('1','3 by 6'),
        ('2','6 by 9')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # domestic_flushing_source = models.CharField(choices=source_choices, max_length=50)
    # toilet_flushing_source = models.CharField(choices=source_choices, max_length=50)
    domestic_flushing_source = models.ManyToManyField(GuestRoomDomesticSource, related_name='guestroom')
    toilet_flushing_source = models.ManyToManyField(GuestRoomToiletSource, related_name='guest_room')
    water_consumption = models.FloatField()
    commode_types = models.CharField(choices=types_of_commodes, max_length=50)
    washbasin_tap_flowrate = models.FloatField()
    toilet_health_faucet_flowrate = models.FloatField()
    def get_domestic_flushing_source_display(self):
        return dict(self.source_choices).get(self.domestic_flushing_source, "Unknown")  
    def get_toilet_flushing_source_display(self):
        return dict(self.source_choices).get(self.toilet_flushing_source, "Unknown")  
    def get_commode_type_display(self):
        return dict(self.types_of_commodes).get(self.commode_types, "Unknown")  
    

class OtherGuestRoomSource(models.Model):
    guestroom_consumption = models.ForeignKey(GuestRoomConsumption, on_delete=models.CASCADE, related_name='other_guestroom_sources')
    name = models.CharField(max_length=255) 

    def __str__(self):
        return self.name  

class EmployeeRoomDomesticSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name  

class EmployeeRoomToiletSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name  
    

class EmployeeRoomConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    types_of_commodes = [
        ('1','3 by 6'),
        ('2','6 by 9')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # domestic_flushing_source = models.CharField(choices=source_choices, max_length=50)
    # toilet_flushing_source = models.CharField(choices=source_choices, max_length=50)
    domestic_flushing_source = models.ManyToManyField(EmployeeRoomDomesticSource, related_name='employeeroom')
    toilet_flushing_source = models.ManyToManyField(EmployeeRoomToiletSource, related_name='employee_room')
    water_consumption = models.FloatField()
    commode_types = models.CharField(choices=types_of_commodes, max_length=50)
    washbasin_tap_flowrate = models.FloatField()
    toilet_health_faucet_flowrate = models.FloatField()
    def get_domestic_flushing_source_display(self):
        return dict(self.source_choices).get(self.domestic_flushing_source, "Unknown")  
    def get_toilet_flushing_source_display(self):
        return dict(self.source_choices).get(self.toilet_flushing_source, "Unknown")  
    def get_commode_type_display(self):
        return dict(self.types_of_commodes).get(self.commode_types, "Unknown")


class OtherEmployeeRoomSource(models.Model):
    employeeroom_consumption = models.ForeignKey(EmployeeRoomConsumption, on_delete=models.CASCADE, related_name='other_guestroom_sources')
    name = models.CharField(max_length=255) 

    def __str__(self):
        return self.name


class DriversRoomDomesticSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name  

class DriversRoomToiletSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name      
    

class DriversRoomConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    types_of_commodes = [
        ('1','3 by 6'),
        ('2','6 by 9')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # domestic_flushing_source = models.CharField(choices=source_choices, max_length=50)
    # toilet_flushing_source = models.CharField(choices=source_choices, max_length=50)
    domestic_flushing_source = models.ManyToManyField(DriversRoomDomesticSource, related_name='employeeroom')
    toilet_flushing_source = models.ManyToManyField(DriversRoomToiletSource, related_name='employee_room')
    water_consumption = models.FloatField()
    commode_types = models.CharField(choices=types_of_commodes, max_length=50)
    washbasin_tap_flowrate = models.FloatField()
    toilet_health_faucet_flowrate = models.FloatField()
    def get_domestic_flushing_source_display(self):
        return dict(self.source_choices).get(self.domestic_flushing_source, "Unknown")  
    def get_toilet_flushing_source_display(self):
        return dict(self.source_choices).get(self.toilet_flushing_source, "Unknown")  
    def get_commode_type_display(self):
        return dict(self.types_of_commodes).get(self.commode_types, "Unknown") 


class OtherDriversRoomSource(models.Model):
    driversroom_consumption = models.ForeignKey(DriversRoomConsumption, on_delete=models.CASCADE, related_name='other_guestroom_sources')
    name = models.CharField(max_length=255) 

    def __str__(self):
        return self.name     


class SwimmingPoolSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class SwimmingPoolConsumption(models.Model):

    reject_to_choices = [
    ('1','ETP'),
    ('2','STP'),
    ('3','Municipal Line')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # swimming_pool_source = models.CharField(max_length=50, choices=source_choices)
    swimming_pool_source = models.ManyToManyField(SwimmingPoolSource, related_name='consumptions')

    total_daily_makeup_water = models.FloatField()
    capacity = models.FloatField()
    reject_to = models.CharField(max_length=255, choices=reject_to_choices)
    reject_to_vol = models.FloatField()

class OtherSwimmingSource(models.Model):
    swimming_pool_consumption = models.ForeignKey(SwimmingPoolConsumption, on_delete=models.CASCADE, related_name='other_swimming_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class WaterBodiesSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name    


class WaterBodiesConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    reject_to_choices = [
    ('1','ETP'),
    ('2','STP'),
    ('3','Municipal Line')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # water_body_source = models.CharField(max_length=50, choices=source_choices)
    water_body_source = models.ManyToManyField(WaterBodiesSource, related_name='waterbody')
    daily_makeup_water = models.FloatField()
    capacity = models.FloatField()
    reject_to = models.CharField(max_length=255, choices=reject_to_choices)
    reject_to_vol = models.FloatField()


class OtherWaterBodiesSource(models.Model):
    water_body_consumption = models.ForeignKey(WaterBodiesConsumption, on_delete=models.CASCADE, related_name='other_waterbody_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name  


class LaundrySource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name       


class LaundryConsumption(ComputedFieldsModel):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    reject_to_choices = [
    ('1','ETP'),
    ('2','STP'),
    ('3','Municipal Line')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # laundry_source = models.CharField(max_length=50, choices=source_choices)
    laundry_source = models.ManyToManyField(LaundrySource, related_name='laundry')
    input_vol = models.FloatField()
    reject_to = models.CharField(max_length=255, choices=reject_to_choices)
    reject_to_vol = models.FloatField()
    washingmachine_capacity = models.FloatField()
    avg_num_solid_clothes = models.FloatField()
    
    @computed(models.FloatField())
    def water_consumption_per_kg_solid_clothes(self):
        return self.input_vol/self.avg_num_solid_clothes 
    

    @computed(models.FloatField())
    def avg_no_of_cycles(self):
        return (0.8*self.washingmachine_capacity)/self.avg_num_solid_clothes
    

class OtherLaundrySource(models.Model):
    laundry_consumption = models.ForeignKey(LaundryConsumption, on_delete=models.CASCADE, related_name='other_laundry_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name     

class BoilerSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class BoilerConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    blowdown_choices = [
        ('1','ETP'),
        ('2','STP'),
        ('3','Municipal Line')
    ]
    pre_treatment_choices = [
        ('1', 'No'),
        ('2', 'Yes')
    ]
    steam_recovery_choices = [
        ('1', 'No'),
        ('2', 'Yes')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # boiler_source = models.CharField(max_length=50, choices=source_choices)
    boiler_source = models.ManyToManyField(BoilerSource, related_name='boiler')
    pre_treatment_boiler = models.CharField(max_length=50, choices=pre_treatment_choices)
    boiler_units = models.IntegerField()
    steam_recovery = models.CharField(max_length=50, choices=steam_recovery_choices)
    recovery_rate = models.FloatField(null=True)


class OtherBoilerSource(models.Model):
    boiler_consumption = models.ForeignKey(BoilerConsumption, on_delete=models.CASCADE, related_name='other_laundry_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name    


class BoilerTreatmentMethods(models.Model):
    treatment_types = [
            ('Pressure Sand Filter(PSF)or Multi Grade Filter(MGF)',
             'Pressure Sand Filter(PSF)or Multi Grade Filter(MGF)'),
            ('Iron Removal Filters(IRF)', 'Iron Removal Filters(IRF)'),
            ('Activated Carbon Filter (ACF)', 'Activated Carbon Filter (ACF)'),
            ('Softener', 'Softener'),
            ('Ultrafiltration(UF)', 'Ultrafiltration(UF)'),
            ('Reverse Osmosis(RO)', 'Reverse Osmosis(RO)'),
            ('Others', 'Others'),
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    boiler = models.ForeignKey(BoilerConsumption, on_delete=models.CASCADE, null=True, blank=True) 
    pre_treatment_boiler_choices = models.CharField(max_length=255, choices=treatment_types, null=True)


class AddBoilerConsumption(models.Model):
    blowdown_choices = [
        ('1','ETP'),
        ('2','STP'),
        ('3','Municipal Line')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    boiler_name = models.CharField(max_length=255, null=True)
    capacity = models.FloatField()
    avg_running_time = models.FloatField()
    blowdown_to = models.CharField(max_length=255, choices=blowdown_choices)
    blowdown_to_vol = models.FloatField()
    blowdown_frequency = models.IntegerField()


class CalorifierSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class CalorifierConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    calorifier_source = models.ManyToManyField(CalorifierSource, related_name='calorifier')
    capacity = models.FloatField()
    water_consumed = models.FloatField()


class OtherCalorifierSource(models.Model):
    calorifier_consumption = models.ForeignKey(CalorifierConsumption, on_delete=models.CASCADE, related_name='other_laundry_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name     


class CoolingTowerConsumption(models.Model):
    coolingtower_type_choices = [
        ('Conventional', 'Conventional'),
        ('Adiabatic', 'Adiabatic')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    coolingtower_type = models.CharField(max_length=255, choices=coolingtower_type_choices)
    freshwater_consumed = models.FloatField()
    treated_wastewater_consumed = models.FloatField()
    blowdown_vol = models.FloatField()


class AddCoolingTowerSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name    


class AddCoolingTowerConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    blowdown_choices = [
        ('1','ETP'),
        ('2','STP'),
        ('3','Municipal Line')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    coolingtower_name = models.CharField(max_length=255, null=True)
    cooling_tower_source = models.ManyToManyField(AddCoolingTowerSource, related_name='add_cooling_tower')
    capacity = models.FloatField()
    blowdown_volume = models.FloatField()
    blowdown_to = models.CharField(max_length=255, choices=blowdown_choices)
    coolingtower_age = models.FloatField()
    coolingtower_coc = models.IntegerField()


class OtherAddCoolingTowerSource(models.Model):
    coolingtower_consumption = models.ForeignKey(AddCoolingTowerConsumption, on_delete=models.CASCADE, related_name='other_laundry_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name    

class IrrigationSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name   
    

class IrrigationConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    irrigation_frequency_options = [
        ('Daily', 'Daily'),
        ('Once in 2 days', 'Once in 2 days'),
        ('Weekly', 'Weekly'),
        ('Others', 'Others')
    ]
    irrigation_technique_options = [
        ('Manual', 'Manual'),
        ('Drip', 'Drip'),
        ('Sprinklers', 'Sprinklers'),
        ('Others', 'Others')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    daily_water_consumption = models.FloatField()
    irrigation_source = models.ManyToManyField(IrrigationSource, related_name='irrigation')
    amount_consumed = models.FloatField()
    lawn_area = models.FloatField()
    irrigation_frequency = models.CharField(max_length=255, choices=irrigation_frequency_options)
    other_irrigation_frequency = models.CharField(max_length=255, null=True)
    irrigation_technique = models.CharField(max_length=255, choices=irrigation_technique_options)
    other_irrigation_technique = models.CharField(max_length=255, null=True)


class OtherIrrigationSource(models.Model):
    irrigation_consumption = models.ForeignKey(IrrigationConsumption, on_delete=models.CASCADE, related_name='other_irrigation_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class OtherConsumptionSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name        


class OtherConsumption(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    reject_to_choices = [
        ('1','ETP'),
        ('2','STP'),
        ('3','Municipal Line')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    process_type = models.CharField(max_length=255)
    other_source = models.ManyToManyField(OtherConsumptionSource, related_name='other_consumption')
    amount_consumed = models.FloatField()
    reject_to = models.CharField(max_length=255, choices=reject_to_choices)
    car_wash = models.FloatField()
    others = models.CharField(max_length=255, null=True)


class OtherConsumptionOtherSource(models.Model):
    other_consumption = models.ForeignKey(OtherConsumption, on_delete=models.CASCADE, related_name='other_consumption_sources')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name    


class WasteWaterTreatment(models.Model):
    treatment_method_choices = [
        ('STP','STP'),
        ('ETP','ETP'),
        ('Others','Others')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    treatment_method = models.CharField(max_length=255, choices=treatment_method_choices)


class WasteWaterTreatmentSTP(models.Model):
    technology_type_choices = [
        ('Activated Sludge Process', 'Activated Sludge Process'),
        ('Sequential Bioreactor (SBR)', 'Sequential Bioreactor (SBR)'),
        ('Membrane BioR', 'Membrane BioR'),
        ('Moving bed biofilm reactor', 'Moving bed biofilm reactor'),
        ('Others','Others')
    ]
    treatment_method_choices = [
        ('Bar screening', 'Bar screening'),
        ('Equalization Tank', 'Equalization Tank'),
        ('Primary settling Tank', 'Primary settling Tank'),
        ('Secondary Tank', 'Secondary Tank'),
        ('Pressure and filter (PSF)', 'Pressure and filter (PSF)'),
        ('Activated carbon filter (ACF)', 'Activated carbon filter (ACF)'),
        ('Softener', 'Softener'),
        ('Ultrafiltration (UF)', 'Ultrafiltration (UF)'),
        ('Sludge holding tank', 'Sludge holding tank'),
        ('Sludge drying bed', 'Sludge drying bed'),
        ('Others', 'Others')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    technology_type = models.CharField(max_length=255,choices=technology_type_choices)
    other_technology_type_name = models.CharField(max_length=255)
    capacity = models.FloatField()
    treatment_method = models.CharField(max_length=255,choices=treatment_method_choices)
    input_volume = models.FloatField()
    output_volume = models.FloatField()


class WasteWaterTreatmentETP(models.Model):
    sequence_flow_choices = [
        ('Bar screening', 'Bar screening'),
        ('Equalization Tank', 'Equalization Tank'),
        ('Coagulation', 'Coagulation'),
        ('Secondary Settling Tank', 'Secondary Settling Tank'),
        ('Pressure and filter (PSF)', 'Pressure and filter (PSF)'),
        ('Activated carbon filter (ACF)', 'Activated carbon filter (ACF)'),
        ('Others', 'Others')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    flow_process = models.CharField(max_length=255)
    capacity = models.FloatField()
    input_flow_vol = models.FloatField()
    technology_type = models.CharField(max_length=255)
    sequence_flow = models.CharField(max_length=255, choices=sequence_flow_choices)
    other_sequence_flow = models.CharField(max_length=255, null=True)
    treated_water_output = models.FloatField()
    treated_water_usage = models.FloatField()
    # percentage_reuse = models.FloatField()         # to be calculated
    reject_to = models.CharField(max_length=255)
    product_to = models.CharField(max_length=255)


class WasteWaterTreatmentOthers(models.Model):
    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    treatment_method = models.CharField(max_length=255)
    capacity = models.FloatField()
    input_flow_vol = models.FloatField()
    product_vol = models.FloatField()
    reject_vol = models.FloatField()
    reject_to = models.CharField(max_length=255)   # (Hint – recycled or discarded)
    product_to = models.CharField(max_length=255)  # (Hint – reused or discarded)

class TanksAndCapacitiesSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name    

class TanksAndCapacities(models.Model):
    source_choices = [
        ('Input freshwater tank','Input freshwater tank'),
        ('Fire tank','Fire tank'),
        ('Softener Storage tank','Softener Storage tank'),
        ('RO Storage tank','RO Storage tank'),
        ('Flush tank','Flush tank'),
        ('Domestic Water tank','Domestic Water tank'),
        ('RO Input tank','RO Input tank'),
        ('Boiler Makeup tank','Boiler Makeup tank'),
    ]
    sequence_flow_choices = [
        ('Input wastewater Tank', 'Input wastewater Tank'),
        ('Equalization Tank', 'Equalization Tank'),
        ('Settling Tank', 'Settling Tank'),
        ('Treated wastewater Tank', 'Treated wastewater Tank'),
        ('Softener storage Tank', 'Softener storage Tank'),
        ('Ultrafiltration (UF)', 'Ultrafiltration (UF)'),
        ('Others', 'Others')
    ]
    technology_type_choices = [
        ('Sequential Bioreactor (SBR)', 'Sequential Bioreactor (SBR)'),
        ('Membrane BioR', 'Membrane BioR'),
        ('Moving bed biofilm reactor', 'Moving bed biofilm reactor')
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    tank_name = models.CharField(max_length=255)
    tank_source = models.ManyToManyField(TanksAndCapacitiesSource, related_name='tanks_and_capacities')
    capacity = models.FloatField()
    sequence_flow = models.CharField(max_length=255, choices=sequence_flow_choices)
    other_sequence_flow = models.CharField(max_length=255, null=True)
    technology_type = models.CharField(max_length=255, choices=technology_type_choices)


class OtherTanksAndCapacitiesSource(models.Model):
    other_consumption = models.ForeignKey(TanksAndCapacities, on_delete=models.CASCADE, related_name='other_tanks_and_capacities')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name     


class WaterQualityProfile(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    pH = models.FloatField()
    chlorides = models.FloatField()
    alkalinity = models.FloatField()
    hardness = models.FloatField()
    turbidity = models.FloatField()
    res_chlorine = models.FloatField()
    iron = models.FloatField()
    nitrate = models.FloatField()
    bod = models.FloatField()
    cod = models.FloatField()
    tss = models.FloatField()


class RecycledWaterProfile(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    usage = models.FloatField()
    place = models.CharField(max_length=255)
    quantity = models.FloatField()


