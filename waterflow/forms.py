from django import forms
from .models import (
    Registration,
    BasicDetails,
    SourceWaterProfile,
    RainWaterProfile,
    FreshWaterTreatmentProfile,
    FreshWaterTreatmentProfileDetails,
    SourceWaterFlow,
    TanksCapacities,
    KitchenDishwasherTapConsumption,
    DrinkingWaterSource,
    RestaurantConsumption,
    BanquetConsumption,
    GuestRoomConsumption,
    EmployeeRoomConsumption,
    DriversRoomConsumption,
    SwimmingPoolConsumption,
    WaterBodiesConsumption,
    LaundryConsumption,
    BoilerConsumption,
    BoilerTreatmentMethods,
    AddBoilerConsumption,
    CalorifierConsumption,
    CoolingTowerConsumption,
    AddCoolingTowerConsumption,
    IrrigationConsumption,
    OtherConsumption,
    WasteWaterTreatment,
    WasteWaterTreatmentSTP,
    WasteWaterTreatmentETP,
    WasteWaterTreatmentOthers,
    TanksAndCapacities,
    WaterQualityProfile,
    RecycledWaterProfile,
)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            "first_name",
            "last_name",
            "company_name",
            "designation",
            "email",
            "mobile_number",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your last name"}
            ),
            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your company name",
                }
            ),
            "designation": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your designation"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            "mobile_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your mobile number",
                    "type": "tel",
                }
            ),
        }


class BasicDetailsForm(forms.ModelForm):
    first_name = (forms.CharField(label="First Name"),)
    last_name = (forms.CharField(),)
    designation = (forms.CharField(),)
    contact_number = (forms.CharField(),)
    email_address = (forms.EmailField(),)
    organization_name = (forms.CharField(),)
    organization_web_address = (forms.URLField(),)
    address = (forms.CharField(),)
    pin_code = (forms.IntegerField(),)
    organization_type = (forms.ChoiceField(required=False,initial='Hospitality'),)
    num_permanent_employees = (forms.IntegerField(),)
    num_temporary_employees = (forms.IntegerField(),)
    num_rooms = (forms.IntegerField(),)
    average_occupancy = (
        forms.IntegerField(
            help_text="Average number of hotel rooms occupied in an year"
        ),
    )
    average_room_occupancy = (forms.IntegerField(help_text="Average number of people in a room"),)
    total_area = (forms.FloatField(label="Total Area (sq.m)"),)
    total_built_up_area = (forms.FloatField(label="Total Built up Area (sq.m)"),)
    total_green_area = (forms.FloatField(label="Total Green Area (sq.m)"),)
    total_air_conditioned_space_area = (
        forms.FloatField(label="Total Air Conditioned Space Area (sq.m)"),
    )

    class Meta:
        org_types = [
            ("1", "Hospitality"),
            ("2", "Industry"),
            ("3", "Buildings"),
        ]
        model = BasicDetails
        fields = [
            "first_name",
            "last_name",
            "designation",
            "contact_number",
            "email_address",
            "organization_name",
            "organization_web_address",
            "address",
            "pin_code",
            "organization_type",
            "num_permanent_employees",
            "num_temporary_employees",
            "num_rooms",
            "average_occupancy",
            "average_room_occupancy",
            "total_area",
            "total_built_up_area",
            "total_green_area",
            "total_air_conditioned_space_area",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your last name"}
            ),
            "designation": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your designation"}
            ),
            "contact_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your contact number",
                }
            ),
            "email_address": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            "organization_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your organization name",
                }
            ),
            "organization_web_address": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter organization web address",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter full address of your organization",
                }
            ),
            "pin_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your pin code"}
            ),
            "organization_type": forms.Select(
                attrs={"class": "form-select","disabled":"disabled"}, choices=org_types
            ),
            "num_permanent_employees": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter number of permanent employees",
                }
            ),
            "num_temporary_employees": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the number of temporary employees",
                }
            ),
            "num_rooms": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the total number of rooms",
                }
            ),
            "average_occupancy": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the average number of rooms occupied in a year",
                }
            ),
            "average_room_occupancy": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the average number of people in a room",
                }
            ),
            "total_area": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter the total area"}
            ),
            "total_built_up_area": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the total built-up area",
                }
            ),
            "total_green_area": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the total green area",
                }
            ),
            "total_air_conditioned_space_area": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the total area of the air-conditioned space",
                }
            ),
        }


class SourceWaterProfileForm(forms.ModelForm):
    source_name = forms.ChoiceField(
        choices=[
            ("1", "Borewell Water"),
            ("2", "Tanker water"),
            ("3", "Metro/corporation Water"),
            ("4", "Rainwater"),
            ("5", "Others"),
        ],
        label="Name of the Source",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    source_daily_consumption = forms.FloatField(
        label="Daily Water Consumption from this Source (kl)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    source_water_cost = forms.FloatField(
        label="Cost of Water from this Source ₹",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = SourceWaterProfile
        fields = ["source_name", "source_daily_consumption", "source_water_cost"]


class RainWaterProfileForm(forms.ModelForm):
    class Meta:
        model = RainWaterProfile
        fields = [
            "amount_harvested_water_last_two_years",
            "amount_recharged_water_last_two_years",
            "rooftop_area",
            "paved_area",
            "unpaved_area",

        ]
        widgets = {
            "amount_harvested_water_last_two_years": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "amount_recharged_water_last_two_years": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "rooftop_area": forms.NumberInput(attrs={"class": "form-control"}),
            "paved_area": forms.NumberInput(attrs={"class": "form-control"}),
            "unpaved_area": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "amount_harvested_water_last_two_years": "Harvested Water in Last 2 Years (kl)",
            "amount_recharged_water_last_two_years": "Recharged Water in Last 2 Years (kl)",
            "rooftop_area": "Rooftop Area (sq. meters)",
            "paved_area": "Paved Area (sq. meters)",
            "unpaved_area": "Unpaved Area (sq. meters)",
        }


class FreshWaterTreatmentProfileForm(forms.ModelForm):
    class Meta:
        treatment_types = [
            (
                "Pressure Sand Filter(PSF)or Multi Grade Filter(MGF)",
                "Pressure Sand Filter(PSF)or Multi Grade Filter(MGF)",
            ),
            ("Iron Removal Filters(IRF)", "Iron Removal Filters(IRF)"),
            ("Activated Carbon Filter (ACF)", "Activated Carbon Filter (ACF)"),
            ("Softener", "Softener"),
            ("Ultrafiltration(UF)", "Ultrafiltration(UF)"),
            ("Reverse Osmosis(RO)", "Reverse Osmosis(RO)"),
            ("Others", "Others"),
        ]

        model = FreshWaterTreatmentProfile
        fields = ["name"]

        widgets = {
            "name": forms.Select(
                attrs={"class": "form-select"}, choices=treatment_types
            )
        }


class FreshWaterTreatmentProfileDetailsForm(forms.ModelForm):
    reject_to = forms.ChoiceField(
        choices=[("1", "ETP"), ("2", "STP"), ("3", "Municipal Line")],
        label="Reject to",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = FreshWaterTreatmentProfileDetails
        fields = [
            "input_water",
            "product_water",
            "reject_water",
            "reject_to",
            "backwash_time",
            "rinse_time",
            "flush_time",
            "regeneration_time",
            "frequency_of_backwash_and_rinse",
            "frequency_of_regeneration",
            "amount_of_water_for_brine_solution",
        ]
        widgets = {
            "input_water": forms.NumberInput(attrs={"class": "form-control"}),
            "product_water": forms.NumberInput(attrs={"class": "form-control"}),
            "reject_water": forms.NumberInput(attrs={"class": "form-control"}),
            "backwash_time": forms.NumberInput(attrs={"class": "form-control"}),
            "rinse_time": forms.NumberInput(attrs={"class": "form-control"}),
            "flush_time": forms.NumberInput(attrs={"class": "form-control"}),
            "regeneration_time": forms.NumberInput(attrs={"class": "form-control"}),
            "frequency_of_backwash_and_rinse": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "frequency_of_regeneration": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "amount_of_water_for_brine_solution": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FreshWaterTreatmentProfileDetailsForm, self).__init__(*args, **kwargs)
        self.fields["input_water"].label = "Input Water (kl)"
        self.fields["product_water"].label = "Product Water (kl)"
        self.fields["reject_water"].label = "Reject Water (kl)"
        # self.fields['reject_to'].label = "Reject to"
        self.fields["backwash_time"].label = "Backwash Time(min/day)"
        self.fields["rinse_time"].label = "Rinse Time(min/day)"
        self.fields["flush_time"].label = "Flush Time(min/day)"
        self.fields["regeneration_time"].label = "Regeneration Time(min/day)"
        self.fields["frequency_of_backwash_and_rinse"].label = (
            "Frequency of Backwash and Rinse(per day)"
        )
        self.fields["frequency_of_regeneration"].label = "Frequency of Regeneration"
        self.fields["amount_of_water_for_brine_solution"].label = (
            "Amount of Water for Brine Solution(kl)"
        )

    def clean(self):
        return super().clean()


class TanksCapacitiesForm(forms.ModelForm):
    name = forms.ChoiceField(
        choices=[
            ("1", "Input freshwater tank"),
            ("2", "Fire tank"),
            ("3", "Softener Storage tank"),
            ("4", "RO Storage tank"),
            ("5", "Flush tank"),
            ("7", "Domestic Water tank"),
            ("8", "RO Input tank"),
            ("9", "Boiler Makeup tank"),
            ("10", "Others"),
        ],
        label="Name of the Tank",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    capacity = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the capacity of the tank",
            }
        ),
        label="Capacity (kl)",
    )

    other_tank_name = forms.CharField(
        required=False,
        label="Name (Others)",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the name of the tank if you chose Others in the name field",
            }
        ),
    )

    class Meta:
        model = TanksCapacities
        fields = ["name", "capacity", "other_tank_name"]


class SourceWaterFlowForm(forms.ModelForm):
    source = forms.ChoiceField(choices=(),widget=forms.Select(attrs={'class': 'form-control'}))
    destination = forms.ChoiceField(choices=(),widget=forms.Select(attrs={'class': 'form-control'}))
    def __init__(self, sources=None, destinations=None,*args, **kwargs):
        self.source_choices = sources
        self.destination_choices = destinations
        super(SourceWaterFlowForm, self).__init__(*args,**kwargs)
        self.fields['source'].choices = self.source_choices
        self.fields['destination'].choices = self.destination_choices    
    class Meta:
        model = SourceWaterFlow
        fields = ['source','destination']


class DrinkingWaterSourceForm(forms.ModelForm):
    class Meta:
        model = DrinkingWaterSource
        fields = [
            "source_name",
            "other_source_name",
            "source",
            "consumption",
            "cost",
            "used_by",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    source_name = forms.ChoiceField(
        choices=DrinkingWaterSource.source_name_choices,
        label="Drinking Water Source",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_source_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter other source",
            }
        ),
    )

    source = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": widget_classes, "placeholder": "Enter the source of water"}
        )
    )

    consumption = forms.FloatField(
        label = "Drinking water consumption (kl)",
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the volume of consumption",
            }
        )
    )

    cost = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the cost of water"}
        )
    )

    used_by = forms.ChoiceField(
        choices=DrinkingWaterSource.used_by_choices,
        label="Used By",
        widget=forms.Select(attrs={"class": widget_classes}),
    )


class KitchenDishwasherTapConsumptionForm(forms.ModelForm):
    kitchen_type = forms.ChoiceField(
        choices=KitchenDishwasherTapConsumption.kitchen_types,
        label="Type of Kitchen",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    volume_consumed = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the volume of water consumed",
            }
        )
    )
    average_customers_per_day = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the average number of customers per day",
            }
        )
    )
    cleaning = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the water consumption in cleaning",
            }
        )
    )
    reject_to = forms.ChoiceField(
        choices=KitchenDishwasherTapConsumption.reject_to_choices,
        label="Reject To",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    reject_volume = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the volume of reject water",
            }
        )
    )
    dishwasher_loads = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the number of loads in dishwasher",
            }
        )
    )
    consumption_per_load = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the consumption per load",
            }
        )
    )
    # handwash_tap_number = forms.FloatField(
    #     widget=forms.NumberInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Enter the number of filling taps",
    #         }
    #     )
    # )
    handwash_tap_flowrate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the flowrate of filling taps",
            }
        )
    )
    handwash_tap_runtime = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the runtime of filling taps",
            }
        )
    )
    # cleaning_tap_number = forms.FloatField(
    #     widget=forms.NumberInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Enter the number of cleaning taps",
    #         }
    #     )
    # )
    cleaning_tap_flowrate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the flowrate of filling taps",
            }
        )
    )
    cleaning_tap_runtime = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the runtime of cleaning taps",
            }
        )
    )

    class Meta:
        model = KitchenDishwasherTapConsumption
        fields = [
            "kitchen_type",
            "average_customers_per_day",
            "volume_consumed",
            "cleaning",
            "reject_to",
            "reject_volume",
            "dishwasher_loads",
            "consumption_per_load",
            # "handwash_tap_number",
            "handwash_tap_flowrate",
            "handwash_tap_runtime",
            # "cleaning_tap_number",
            "cleaning_tap_flowrate",
            "cleaning_tap_runtime",
        ]


class RestaurantConsumptionForm(forms.ModelForm):
    class Meta:
        model = RestaurantConsumption
        fields = [
            "restaurant_name",
            "accessible",
            "average_occupancy",
            "reject_to",
            "tap_flowrate",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    restaurant_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": widget_classes, "placeholder": "Enter restaurant name"}
        )
    )

    accessible = forms.ChoiceField(
        choices=RestaurantConsumption.accessible_choices,
        label="Accessible",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    average_occupancy = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the average occupancy per day",
            }
        )
    )

    reject_to = forms.ChoiceField(
        choices=RestaurantConsumption.reject_to_choices,
        label="Reject To",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    tap_flowrate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the flow rate of taps",
            }
        )
    )



class BanquetConsumptionForm(forms.ModelForm):
    class Meta:
        model = BanquetConsumption
        fields = [
            "banquet_name",
            "seating_capacity",
            "average_occupancy",
            "drinking_water_source",
            "drinking_water_consumed",
            "tap_flowrate",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    banquet_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": widget_classes, "placeholder": "Enter banquet name"}
        )
    )

    seating_capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter seating capacity of banquet",
            }
        )
    )

    average_occupancy = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the average occupancy",
            }
        )
    )

    drinking_water_source = forms.ChoiceField(
        choices=[
            ("1", "In House RO System"),
            ("2", "Bottled Water"),
            ("3", "Individual RO Purifiers"),
            ("4", "Others"),
        ],
        label="Drinking Water Source",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    drinking_water_consumed = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the volume consumed"}
        )
    )

    tap_flowrate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the flow rate"}
        )
    )


class GuestRoomConsumptionForm(forms.ModelForm):
    class Meta:
        model = GuestRoomConsumption
        fields = ["domestic_flushing_source",
                  "toilet_flushing_source",
                  "water_consumption",
                  "commode_types",
                  "washbasin_tap_flowrate",
                  "toilet_health_faucet_flowrate"
                ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    domestic_flushing_source = forms.ChoiceField(
        widget=forms.Select(
            attrs={"class": widget_classes, "placeholder": "Enter the source of domestic flushing water"}
        ),
        label = "Domestic Flushing Source",
        choices=GuestRoomConsumption.source_choices,        
    )

    toilet_flushing_source = forms.ChoiceField(
        choices=GuestRoomConsumption.source_choices,
        label="Toilet Flushing Source",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    water_consumption = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the specific water consumed per room"}
        ),
        label = "Specific Water Consumption Per Room",
    )

    commode_types = forms.ChoiceField(
        choices=GuestRoomConsumption.types_of_commodes,
        widget=forms.Select(
            attrs={"class": widget_classes, "placeholder": "Enter the type of commodes"}
        ),
        label = "Enter the type of commodes",
    )

    washbasin_tap_flowrate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the flow rate of washbasin tap"}
        ),
        label = "Washbasin Tap Flowrate",
    )

    toilet_health_faucet_flowrate = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the flowrate of health faucets",
            }
        ),
        label = "Toilet Heatlh Faucets Flowrate",
    )


class EmployeeRoomConsumptionForm(forms.ModelForm):
    class Meta:
        model = EmployeeRoomConsumption
        fields = [
            "domestic_flushing_source",
            "toilet_flushing_source",
            "water_consumption",
            "commode_types",
            "washbasin_tap_flowrate",
            "toilet_health_faucet_flowrate",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    domestic_flushing_source = forms.ChoiceField(
        choices=EmployeeRoomConsumption.source_choices,
        label= "Domestic Flushing Source",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    toilet_flushing_source = forms.ChoiceField(
        choices=EmployeeRoomConsumption.source_choices,
        label="Toilet Flushing Source",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    water_consumption = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the specific water consumption per room",
            }
        )
    )

    commode_types = forms.ChoiceField(
        choices=EmployeeRoomConsumption.types_of_commodes,
        label= "Commode Type",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    washbasin_tap_flowrate = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the number of restrooms",
            }
        )
    )

    toilet_health_faucet_flowrate = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the number of restrooms",
            }
        )
    )


class DriversRoomConsumptionForm(forms.ModelForm):
    class Meta:
        model = DriversRoomConsumption
        fields = ["domestic_flushing_source",
                  "toilet_flushing_source",
                  "water_consumption",
                  "commode_types",
                  "washbasin_tap_flowrate",
                  "toilet_health_faucet_flowrate"
                ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    domestic_flushing_source = forms.ChoiceField(
        widget=forms.Select(
            attrs={"class": widget_classes, "placeholder": "Enter the source of domestic flushing water"}
        ),
        label = "Domestic Flushing Source",
        choices=DriversRoomConsumption.source_choices,        
    )

    toilet_flushing_source = forms.ChoiceField(
        choices=DriversRoomConsumption.source_choices,
        label="Toilet Flushing Source",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    water_consumption = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the specific water consumed per room"}
        ),
        label = "Specific Water Consumption Per Room",
    )

    commode_types = forms.ChoiceField(
        choices=DriversRoomConsumption.types_of_commodes,
        widget=forms.Select(
            attrs={"class": widget_classes, "placeholder": "Enter the type of commodes"}
        ),
        label = "Enter the type of commodes",
    )

    washbasin_tap_flowrate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the flow rate of washbasin tap"}
        ),
        label = "Washbasin Tap Flowrate",
    )

    toilet_health_faucet_flowrate = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the flowrate of health faucets",
            }
        ),
        label = "Toilet Heatlh Faucets Flowrate",
    )


class SwimmingPoolConsumptionForm(forms.ModelForm):
    class Meta:
        model = SwimmingPoolConsumption
        fields = [
            "swimming_pool_source",
            "total_daily_makeup_water",
            "capacity",
            "reject_to",
            "reject_to_vol",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    swimming_pool_source = forms.ChoiceField(
        choices=SwimmingPoolConsumption.source_choices,
        label="Water source choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    total_daily_makeup_water = forms.FloatField(
        label = 'Total Daily Makeup Water (kl)',
        widget=forms.NumberInput(attrs={
            "class": widget_classes,
            "placeholder": "Enter the total daily makeup water"}),
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter capacity of swimming pools",
            }
        )
    )

    reject_to = forms.ChoiceField(
        choices=SwimmingPoolConsumption.reject_to_choices,
        label="Reject To",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    reject_to_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter volume of water rejected",
            }
        )
    )


class WaterBodiesConsumptionForm(forms.ModelForm):
    class Meta:
        model = WaterBodiesConsumption
        fields = [
            "water_body_source",
            "daily_makeup_water",
            "capacity",
            "reject_to",
            "reject_to_vol",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    water_body_source = forms.ChoiceField(
        choices=WaterBodiesConsumption.source_choices,
        label="Water source choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    daily_makeup_water = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the daily makeup of water bodies",
            }
        )
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the capacity of water bodies",
            }
        )
    )

    reject_to = forms.ChoiceField(
        choices=WaterBodiesConsumption.reject_to_choices,
        label="Reject To",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    reject_to_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter volume of water rejected",
            }
        )
    )


class LaundryConsumptionForm(forms.ModelForm):
    class Meta:
        model = LaundryConsumption
        fields = [
            "laundry_source",
            "input_vol",
            "reject_to",
            "reject_to_vol",
            "washingmachine_capacity",
            "avg_num_solid_clothes",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    laundry_source = forms.ChoiceField(
        choices=WaterBodiesConsumption.source_choices,
        label="Water source choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    input_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the volume of water input",
            }
        )
    )

    reject_to_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter volume of water rejected",
            }
        )
    )

    reject_to = forms.ChoiceField(
        choices=WaterBodiesConsumption.reject_to_choices,
        label="Reject To",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    washingmachine_capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the total solid clothes per day",
            }
        )
    )

    avg_num_solid_clothes = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of solid clothes washed per day",
            }
        )
    )

class BoilerConsumptionForm(forms.ModelForm):
    class Meta:
        model = BoilerConsumption
        fields = [
            "boiler_source",
            "other_source_name",
            "pre_treatment_boiler",
            "boiler_units",
            "steam_recovery",
            "recovery_rate",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    boiler_source = forms.ChoiceField(
        choices=BoilerConsumption.source_choices,
        label="Water source choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_source_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter other source",
            }
        ),
    )

    pre_treatment_boiler = forms.ChoiceField(
        choices=BoilerConsumption.pre_treatment_choices,
        label="Pre-treatment of Water Boiler",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    boiler_units = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the number of boiler units",
            }
        )
    )

    steam_recovery = forms.ChoiceField(
        choices=BoilerConsumption.steam_recovery_choices,
        label="Steam Recovery",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    recovery_rate = forms.FloatField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the recovery rate",
            }
        ),
    )


class BoilerTreatmentMethodsForm(forms.ModelForm):
    class Meta:
        model = BoilerTreatmentMethods
        fields = ["pre_treatment_boiler_choices"]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    pre_treatment_boiler_choices = forms.ChoiceField(
        choices=BoilerTreatmentMethods.treatment_types,
        label="Pre-treatment of Water Boiler Methods",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

class AddBoilerConsumptionForm(forms.ModelForm):
    class Meta:
        model = AddBoilerConsumption
        fields = [
            "boiler_name",
            "capacity",
            "avg_running_time",
            "blowdown_to",
            "blowdown_to_vol",
            "blowdown_frequency"
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    boiler_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": widget_classes, "placeholder": "Enter the name of Boiler"}
        )
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the capacity of boiler",
            }
        )
    )

    avg_running_time = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the average run time"}
        )
    )

    blowdown_to = forms.ChoiceField(
        choices=BoilerConsumption.blowdown_choices,
        label="Reject To",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    blowdown_to_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter volume of water rejected",
            }
        )
    )

    blowdown_frequency = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the frequency of blowdown",
            }
        )
    )

class CalorifierConsumptionForm(forms.ModelForm):
    class Meta:
        model = CalorifierConsumption
        fields = [
            "calorifier_source",
            "other_source_name",
            "capacity",
            "water_consumed",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    calorifier_source = forms.ChoiceField(
        choices=CalorifierConsumption.source_choices,
        label="Water source choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_source_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter other source",
            }
        ),
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the capacity of calorifier",
            }
        )
    )

    water_consumed = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of water consumed",
            }
        )
    )


class CoolingTowerConsumptionForm(forms.ModelForm):
    class Meta:
        model = CoolingTowerConsumption
        fields = [
            "coolingtower_type",
            "freshwater_consumed",
            "treated_wastewater_consumed",
            "blowdown_vol",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    coolingtower_type = forms.ChoiceField(
        choices=CoolingTowerConsumption.coolingtower_type_choices,
        label="Cooling Tower Type",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    freshwater_consumed = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of freshwater consumed",
            }
        )
    )

    treated_wastewater_consumed = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of treated waste water consumed",
            }
        )
    )

    blowdown_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of water blown down",
            }
        )
    )


class AddCoolingTowerConsumptionForm(forms.ModelForm):
    class Meta:
        model = AddCoolingTowerConsumption
        fields = [
            "coolingtower_name",
            "cooling_tower_source",
            "other_source_name",
            "capacity",
            "blowdown_volume",
            "blowdown_to",
            "coolingtower_age",
            "coolingtower_coc",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    coolingtower_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the name of cooling tower",
            }
        )
    )

    cooling_tower_source = forms.ChoiceField(
        choices=AddCoolingTowerConsumption.source_choices,
        label="Water source choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_source_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter other source",
            }
        ),
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the capacity of cooling tower",
            }
        )
    )

    blowdown_volume = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the blowdown volume",
            }
        )
    )

    blowdown_to = forms.ChoiceField(
        choices=AddCoolingTowerConsumption.blowdown_choices,
        label="Blow Down To",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    coolingtower_age = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the age of cooling tower",
            }
        )
    )

    coolingtower_coc = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter cooling tower C.O.C"}
        )
    )


class IrrigationConsumptionForm(forms.ModelForm):
    class Meta:
        model = IrrigationConsumption
        fields = [
            "daily_water_consumption",
            "irrigation_source",
            "other_source_name",
            "amount_consumed",
            "lawn_area",
            "irrigation_frequency",
            "other_irrigation_frequency",
            "irrigation_technique",
            "other_irrigation_technique",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    daily_water_consumption = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter daily water consumption",
            }
        )
    )

    irrigation_source = forms.ChoiceField(
        choices=IrrigationConsumption.source_choices,
        label="Water source choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_source_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter other source",
            }
        ),
    )

    amount_consumed = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of water consumed",
            }
        )
    )

    lawn_area = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the total lawn area"}
        )
    )

    irrigation_frequency = forms.ChoiceField(
        choices=IrrigationConsumption.irrigation_frequency_options,
        label="Irrigation Frequency",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_irrigation_frequency = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter other irrigation frequency",
            }
        ),
    )

    irrigation_technique = forms.ChoiceField(
        choices=IrrigationConsumption.irrigation_technique_options,
        label="Irrigation Techniques",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_irrigation_technique = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter other irrigation technique",
            }
        ),
    )


class OtherConsumptionForm(forms.ModelForm):
    class Meta:
        model = OtherConsumption
        fields = [
            "process_type",
            "other_source",
            "other_source_name",
            "amount_consumed",
            "reject_to",
            "car_wash",
            "others",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    process_type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter consumption process type",
            }
        )
    )

    other_source = forms.ChoiceField(
        choices=OtherConsumption.source_choices,
        label="Water source choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_source_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter other source",
            }
        ),
    )

    amount_consumed = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of water consumed",
            }
        )
    )

    reject_to = forms.ChoiceField(
        choices=OtherConsumption.reject_to_choices,
        label="Reject To",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    car_wash = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of water consumed in car wash",
            }
        )
    )

    others = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": f"{widget_classes} mt-4", "placeholder": "Others"}
        ),
    )


class WasteWaterTreatmentForm(forms.ModelForm):
    class Meta:
        model = WasteWaterTreatment
        fields = ["treatment_method"]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    treatment_method = forms.ChoiceField(
        choices=WasteWaterTreatment.treatment_method_choices,
        label="Treatment method choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )


class WasteWaterTreatmentSTPForm(forms.ModelForm):
    class Meta:
        model = WasteWaterTreatmentSTP
        fields = [
            "technology_type",
            "other_technology_type_name",
            "capacity",
            "treatment_method",
            "input_volume",
            "output_volume",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    technology_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": f"{widget_classes} mt-4",
            }
        ),
        label = "Type of Treatment",
        choices = WasteWaterTreatmentSTP.technology_type_choices,
    )

    other_technology_type_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the name of the technology if you chose other",
            }
        )
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the capacity"}
        )
    )

    treatment_method = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": widget_classes,
            }
        ),
        label = "Enter the treatment method",
        choices = WasteWaterTreatmentSTP.treatment_method_choices,
    )

    input_volume = forms.FloatField(
        label="Input Volume",
        widget=forms.NumberInput(attrs={"class": widget_classes, "placeholder":"Enter the input volume"}),
    )

    output_volume = forms.FloatField(
        label="Output Volume",
        widget=forms.NumberInput(attrs={"class": widget_classes,"placeholder":"Output Volume"}),
    )


class WasteWaterTreatmentETPForm(forms.ModelForm):
    class Meta:
        model = WasteWaterTreatmentETP
        fields = [
            "flow_process",
            "capacity",
            "input_flow_vol",
            "technology_type",
            "sequence_flow",
            "other_sequence_flow",
            "treated_water_output",
            "treated_water_usage",
            "reject_to",
            "product_to",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    flow_process = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the flow process",
            }
        )
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the capacity"}
        )
    )

    input_flow_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the volume of input flow water",
            }
        )
    )

    technology_type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the technology type",
            }
        )
    )

    sequence_flow = forms.ChoiceField(
        choices=WasteWaterTreatmentETP.sequence_flow_choices,
        label="Sequence Flow",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_sequence_flow = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Mention other sequence flow",
            }
        ),
    )

    treated_water_output = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the volume of output treated water",
            }
        )
    )

    treated_water_usage = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the volume of treated water usage",
            }
        )
    )

    reject_to = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "(Hint - recycled or discarded)",
            }
        )
    )

    product_to = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "(Hint - reused or discarded)",
            }
        )
    )


class WasteWaterTreatmentOthersForm(forms.ModelForm):
    class Meta:
        model = WasteWaterTreatmentOthers
        fields = [
            "treatment_method",
            "capacity",
            "input_flow_vol",
            "product_vol",
            "reject_vol",
            "reject_to",
            "product_to",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    treatment_method = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the treatment method",
            }
        )
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the capacity"}
        )
    )

    input_flow_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the volume of incoming water",
            }
        )
    )

    product_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the proudct volume"}
        )
    )

    reject_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the water volume rejected",
            }
        )
    )

    reject_to = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "(Hint - recycled or discarded)",
            }
        )
    )

    product_to = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "(Hint - reused or discarded)",
            }
        )
    )


class TanksAndCapacitiesForm(forms.ModelForm):
    class Meta:
        model = TanksAndCapacities
        fields = [
            "tank_name",
            "tank_source",
            "other_source_name",
            "capacity",
            "sequence_flow",
            "other_sequence_flow",
            "technology_type",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    tank_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the name of the tank",
            }
        )
    )

    tank_source = forms.ChoiceField(
        choices=TanksAndCapacities.source_choices,
        label="Water Sources",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_source_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": widget_classes, "placeholder": "Mention other water source"}
        ),
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the capacity"}
        )
    )

    sequence_flow = forms.ChoiceField(
        choices=TanksAndCapacities.sequence_flow_choices,
        label="Sequence Flow",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_sequence_flow = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Mention other sequence flow",
            }
        ),
    )

    technology_type = forms.ChoiceField(
        choices=TanksAndCapacities.technology_type_choices,
        label="Technology type choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )


class WasteWaterTreatmentOthersForm(forms.ModelForm):
    class Meta:
        model = WasteWaterTreatmentOthers
        fields = [
            "treatment_method",
            "capacity",
            "input_flow_vol",
            "product_vol",
            "reject_vol",
            "reject_to",
            "product_to",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    treatment_method = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the treatment method",
            }
        )
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the capacity"}
        )
    )

    input_flow_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the volume of incoming water",
            }
        )
    )

    product_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the proudct volume"}
        )
    )

    reject_vol = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the water volume rejected",
            }
        )
    )

    reject_to = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "(Hint - recycled or discarded)",
            }
        )
    )

    product_to = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "(Hint - reused or discarded)",
            }
        )
    )


class TanksAndCapacitiesForm(forms.ModelForm):
    class Meta:
        model = TanksAndCapacities
        fields = [
            "tank_name",
            "tank_source",
            "other_source_name",
            "capacity",
            "sequence_flow",
            "other_sequence_flow",
            "technology_type",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    tank_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the name of the tank",
            }
        )
    )

    tank_source = forms.ChoiceField(
        choices=TanksAndCapacities.source_choices,
        label="Water Sources",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_source_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": widget_classes, "placeholder": "Mention other water source"}
        ),
    )

    capacity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": widget_classes, "placeholder": "Enter the capacity"}
        )
    )

    sequence_flow = forms.ChoiceField(
        choices=TanksAndCapacities.sequence_flow_choices,
        label="Sequence Flow",
        widget=forms.Select(attrs={"class": widget_classes}),
    )

    other_sequence_flow = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Mention other sequence flow",
            }
        ),
    )

    technology_type = forms.ChoiceField(
        choices=TanksAndCapacities.technology_type_choices,
        label="Technology type choices",
        widget=forms.Select(attrs={"class": widget_classes}),
    )


class WaterQualityProfileForm(forms.ModelForm):
    class Meta:
        model = WaterQualityProfile
        fields = [
            "pH",
            "chlorides",
            "alkalinity",
            "hardness",
            "turbidity",
            "res_chlorine",
            "iron",
            "nitrate",
            "bod",
            "cod",
            "tss",
        ]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    pH = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the pH level of water",
            }
        )
    )

    chlorides = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of chlorides",
            }
        )
    )

    alkalinity = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of alkanity",
            }
        )
    )

    hardness = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the hardness of water",
            }
        )
    )

    turbidity = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of turbidity",
            }
        )
    )

    res_chlorine = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of residual chlorines",
            }
        )
    )

    iron = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of iron in water",
            }
        )
    )

    nitrate = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of nitrate in water",
            }
        )
    )

    bod = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of B.O.D in water",
            }
        )
    )

    cod = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of C.O.D in water",
            }
        )
    )

    tss = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": f"{widget_classes} mt-4",
                "placeholder": "Enter the level of TSS in water",
            }
        )
    )


class RecycledWaterProfileForm(forms.ModelForm):
    class Meta:
        model = RecycledWaterProfile
        fields = ["usage", "place", "quantity"]

    # Add Tailwind CSS classes for responsiveness
    widget_classes = "block w-full px-3 py-2 border border-blue-800 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    usage = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of usage of recycled water",
            }
        )
    )

    place = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": widget_classes, "placeholder": "Enter the place"}
        )
    )

    quantity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": widget_classes,
                "placeholder": "Enter the quantity of recycled water",
            }
        )
    )
