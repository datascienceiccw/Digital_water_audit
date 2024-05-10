from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import FileResponse
from django.core.serializers import serialize
from .models import (
    SourceWaterProfile,
    RainWaterProfile,
    FreshWaterTreatmentProfile,
    FreshWaterTreatmentMethods,
    BasicDetails,
    FreshWaterTreatmentProfileDetails,
    SourceWaterFlow,
    TanksCapacities,
    TanksCapacitiesSource,
    DrinkingWaterSource,
    DrinkingWaterSystem,
    DrinkingWaterSourceName,
    RestaurantConsumption,
    KitchenDishwasherTapConsumption,
    BanquetConsumption,
    BanquetSource,
    GuestRoomConsumption,
    GuestRoomDomesticSource,
    GuestRoomToiletSource,
    EmployeeRoomConsumption,
    EmployeeRoomDomesticSource,
    EmployeeRoomToiletSource,
    DriversRoomConsumption,
    DriversRoomDomesticSource,
    DriversRoomToiletSource,
    SwimmingPoolConsumption,
    SwimmingPoolSource,
    WaterBodiesConsumption,
    WaterBodiesSource,
    LaundryConsumption,
    LaundrySource,
    BoilerConsumption,
    BoilerSource,
    BoilerTreatmentMethods,
    AddBoilerConsumption,
    CalorifierConsumption,
    CalorifierSource,
    CoolingTowerConsumption,
    AddCoolingTowerConsumption,
    AddCoolingTowerSource,
    IrrigationConsumption,
    IrrigationSource,
    OtherConsumption,
    OtherConsumptionSource,
    WasteWaterTreatment,
    WasteWaterTreatmentSTP,
    WasteWaterTreatmentETP,
    WasteWaterTreatmentOthers,
    TanksAndCapacities,
    TanksAndCapacitiesSource,
    WaterQualityProfile,
    RecycledWaterProfile,
)
from .forms import (
    RegistrationForm,
    BasicDetailsForm,
    SourceWaterProfileForm,
    SourceWaterFlowForm,
    RainWaterProfileForm,
    FreshWaterTreatmentProfileForm,
    FreshWaterTreatmentProfileDetailsForm,
    TanksCapacitiesForm,
    KitchenDishwasherTapConsumptionForm,
    DrinkingWaterSourceForm,
    RestaurantConsumptionForm,
    BanquetConsumptionForm,
    GuestRoomConsumptionForm,
    EmployeeRoomConsumptionForm,
    DriversRoomConsumptionForm,
    SwimmingPoolConsumptionForm,
    WaterBodiesConsumptionForm,
    LaundryConsumptionForm,
    BoilerConsumptionForm,
    BoilerTreatmentMethodsForm,
    AddBoilerConsumptionForm,
    CalorifierConsumptionForm,
    CoolingTowerConsumptionForm,
    AddCoolingTowerConsumptionForm,
    IrrigationConsumptionForm,
    OtherConsumptionForm,
    WasteWaterTreatmentForm,
    WasteWaterTreatmentSTPForm,
    WasteWaterTreatmentETPForm,
    WasteWaterTreatmentOthersForm,
    TanksAndCapacitiesForm,
    WaterQualityProfileForm,
    RecycledWaterProfileForm,
)

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
import json
import plotly
import plotly.graph_objs as go
from .dash_source_app import create_user_dash_app
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from django.forms import modelformset_factory
from reportlab.platypus import HRFlowable, PageBreak


def home_view(request):
    if request.user.is_authenticated:
        return redirect("user_home")
    if request.method == "POST":
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("registration_done/")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, "home.html", {"form": form})


@login_required
def user_home_view(request):
    if not request.session.get("message_seen", False):
        messages.success(request, "")
        request.session["message_seen"] = True
    return render(request, "user_home.html", {"user": request.user})


@login_required
def logout_view(request):
    logout(request)
    # if not request.session.get("message_seen", False):
    #     messages.success(request, "")
    #     request.session["message_seen"] = True
    return HttpResponseRedirect("/")


@login_required
def basic_details(request):  
    current_user = request.user
    details = BasicDetails.objects.filter(user=current_user).first()
    
    if request.method == "POST":
        form = BasicDetailsForm(request.POST, instance=details)
        if form.is_valid():
            basic_details = form.save(commit=False)
            if not details:
                basic_details.user = current_user
            basic_details.save()
            return redirect("source-water-profile/") 
        else:
            for error in form.errors:
                print('Error : ',error)

    else:
        if details:
            form = BasicDetailsForm(instance=details)
        else:
            form = BasicDetailsForm(initial={'organization_type': 'Hospitality'})

    return render(request, "BasicDetails.html", {"form": form})



@login_required
def delete_basic_details(request):
    current_user = request.user
    BasicDetails.objects.filter(user=current_user).delete()
    return redirect("basic_details")


@login_required
def source_water_profile(request):
    if request.method == "POST":
        form = SourceWaterProfileForm(request.POST)
        if form.is_valid():
            current_user = request.user
            form.instance.user = current_user
            names = request.POST.getlist('source_name')
            other_source_name = request.POST.getlist('other_source_name')
            consumptions = request.POST.getlist('source_daily_consumption')
            cost = request.POST.getlist('source_water_cost')
            if names and consumptions and cost:
                for i in range(len(names)):
                    if consumptions[i] and cost[i]:
                        if names[i] == 'Others':
                            source_water_profile = SourceWaterProfile.objects.create(user=current_user, source_name=other_source_name[0], source_daily_consumption=consumptions[i], source_water_cost=cost[i])
                            other_source_name = other_source_name[1:]
                        else:    
                            source_water_profile = SourceWaterProfile.objects.create(user=current_user, source_name=names[i], source_daily_consumption=consumptions[i], source_water_cost=cost[i])
                        source_water_profile.save()
            return redirect("source_water_profile")
        else:
            print(form.errors)
    else:
        form = SourceWaterProfileForm()
    all_sources = SourceWaterProfile.objects.filter(user=request.user)
    return render(
        request, "SourceWaterProfile.html", {"form": form, "all_sources": all_sources}
    )


@login_required
def delete_source_water_profile(request):
    current_user = request.user
    SourceWaterProfile.objects.filter(user=current_user).delete()
    return redirect("source_water_profile")


@login_required
def rainwater(request):  # sourcery skip: assign-if-exp, merge-else-if-into-elif
    current_user = request.user
    details = RainWaterProfile.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = RainWaterProfileForm(request.POST or None)
        if form.is_valid():
            form.instance.user = current_user
            form.save()
            return redirect("source_dash_view")
        else:
            print(form.errors)
    else:
        if details:
            form = RainWaterProfileForm(instance=details)
        else:
            form = RainWaterProfileForm()
    is_rainwater_present = SourceWaterProfile.objects.filter(
        user=current_user, source_name=4
    ).exists()
    return render(
        request,
        "rainwater.html",
        {
            "form": form,
            "details": details,
            "is_rainwater_present": is_rainwater_present,
        },
    )


@login_required
def delete_rainwater(request):
    current_user = request.user
    RainWaterProfile.objects.filter(user=current_user).delete()
    return redirect("rainwater_details")


@login_required
def fresh_water_treatment_profile(request):
    global treatment_methods
    treatment_methods = []
    current_user = request.user
    if request.method == "POST":
        form = FreshWaterTreatmentProfileForm(request.POST)
        if form.is_valid():
            freshwater_treatment = form.save(commit=False)
            freshwater_treatment.user = current_user
            # freshwater_treatment.save()

            other_treatment = form.cleaned_data['name']
            for name in other_treatment:
                name = name.strip()
                if name:
                    treatment_profile = FreshWaterTreatmentProfile.objects.create(user=current_user, name=name)
                    treatment_profile.save()
                    # FreshWaterTreatmentProfile.objects.get_or_create(name=name)

            other_treatment = request.POST.getlist('other_sources')
            if other_treatment:
                for name in other_treatment:
                    if name:
                        treatment_profile = FreshWaterTreatmentProfile.objects.create(user=current_user, name=name)
                        treatment_profile.save()   
                    # FreshWaterTreatmentProfile.objects.get_or_create(name=name)  
            return redirect("fresh_water_treatment_profile")
        else:
            print(form.errors)
    else:
        form = FreshWaterTreatmentProfileForm()

    treatment_methods.clear()
    all_treatment_methods = FreshWaterTreatmentProfile.objects.filter(user=request.user)
    for method in all_treatment_methods:
        treatment_methods.append(method)
    return render(
        request,
        "FreshWaterTreatmentProfile.html",
        {"form": form, "all_treatment_methods": all_treatment_methods},
    )


@login_required
def delete_fresh_water_treatment_profile(request):
    current_user = request.user
    FreshWaterTreatmentProfile.objects.filter(user=current_user).delete()
    return redirect("fresh_water_treatment_profile")


@login_required
def fresh_water_treatment_profile_details(request):
    profiles = FreshWaterTreatmentProfile.objects.filter(user=request.user)
    if request.method == "POST":
        if "reset" in request.POST:
            profile_id_to_reset = request.POST["reset"]
            FreshWaterTreatmentProfileDetails.objects.filter(
                profile_id=profile_id_to_reset
            ).delete()
        else:
            for profile in profiles:
                form = FreshWaterTreatmentProfileDetailsForm(
                    request.POST, prefix=str(profile.id)
                )
                if form.is_valid():
                    details = form.save(commit=False)
                    details.profile = profile
                    details.save()
        return redirect("fresh_water_treatment_profile_details")
    forms = {}
    for profile in profiles:
        details = FreshWaterTreatmentProfileDetails.objects.filter(
            profile=profile
        ).first()

        if details:
            form = FreshWaterTreatmentProfileDetailsForm(
                prefix=str(profile.id), instance=details
            )
        else:
            form = FreshWaterTreatmentProfileDetailsForm(prefix=str(profile.id))

        if profile.name not in [
            "Pressure Sand Filter(PSF)or Multi Grade Filter(MGF)",
            "Iron Removal Filters(IRF)",
            "Activated Carbon Filter (ACF)",
            "Softener",
            "Ultrafiltration(UF)",
        ]:
            if "backwash_time" in form.fields:
                del form.fields["backwash_time"]

            if "rinse_time" in form.fields:
                del form.fields["rinse_time"]

        if profile.name != "Reverse Osmosis(RO)" and "flush_time" in form.fields:
            del form.fields["flush_time"]

        if profile.name != "Softener" and "regeneration_time" in form.fields:
            del form.fields["regeneration_time"]

        if profile.name != "Softener":
            if "frequency_of_regeneration" in form.fields:
                del form.fields["frequency_of_regeneration"]

            if "amount_of_water_for_brine_solution" in form.fields:
                del form.fields["amount_of_water_for_brine_solution"]

        if (
            profile.name
            not in [
                "Pressure Sand Filter(PSF)or Multi Grade Filter(MGF)",
                "Iron Removal Filters(IRF)",
                "Activated Carbon Filter (ACF)",
                "Softener",
                "Ultrafiltration(UF)",
            ]
            and "frequency_of_backwash_and_rinse" in form.fields
        ):
            del form.fields["frequency_of_backwash_and_rinse"]

        forms[profile] = {"form": form, "details": details}
    total_treatment_profile_details = len(
        FreshWaterTreatmentProfileDetails.objects.all()
    )

    all_form_filled = total_treatment_profile_details == len(profiles)
    context = {"forms": forms, "all_form_filled": all_form_filled}

    return render(request, "FreshWaterTreatmentProfileDetails.html", context)


@login_required
def thank_you_view(request, *args, **kwargs):
    return render(request, "thank_you.html", {})


def fresh_water_details_charts():
    # Fetching data from the database
    details = FreshWaterTreatmentProfileDetails.objects.select_related("profile").all()
    profile_names = [detail.profile.name for detail in details]
    input_water = [detail.input_water for detail in details]
    product_water = [detail.product_water for detail in details]
    reject_water = [detail.reject_water for detail in details]

    # Bar Chart: Water Input vs. Product Water vs Reject Water
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=profile_names, y=input_water, name="Input Water"))
    fig1.add_trace(go.Bar(x=profile_names, y=product_water, name="Product Water"))
    fig1.add_trace(go.Bar(x=profile_names, y=reject_water, name="Reject Water"))

    fig1.update_layout(
        title_text="Water Input vs Product Water",
        title_font=dict(
            size=20, family="Arial, sans-serif", color="navy"
        ),  # Title font settings
        paper_bgcolor="rgba(0,0,0,0.1)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        legend=dict(
            # Semi-transparent legend background
            bgcolor="rgba(255, 255, 255, 0.6)",
            bordercolor="Black",
            borderwidth=2,
        ),
        autosize=True,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )

    return json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)


@login_required
def source_water_pie_chart(request):
    current_user = request.user

    # Aggregating daily water consumption by source type
    aggregation = (
        SourceWaterProfile.objects.filter(user=current_user)
        .values("source_name")
        .annotate(total=Sum("source_daily_consumption"))
    )

    # Creating a dictionary to hold the consumption values for each source
    consumption = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    for item in aggregation:
        consumption[item["source_name"]] += item["total"]

    # Extracting the values and converting them into a list
    borewell_volume = consumption["1"]
    tanker_volume = consumption["2"]
    metro_volume = consumption["3"]
    rain_volume = consumption["4"]
    others_volume = consumption["5"]

    total_input_water = sum(
        [borewell_volume, tanker_volume, metro_volume, rain_volume, others_volume]
    )
    if total_input_water == 0:
        return render(
            request, "error_page.html", {"error": "No Water Consumption Data"}
        )

    labels = ["Borewell", "Tanker", "Metro", "Rain", "Others"]
    values = [borewell_volume, tanker_volume, metro_volume, rain_volume, others_volume]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                hoverinfo="label+percent+value",
                hovertemplate="%{label}: %{value} litres<br><extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title_text="Water Consumption Share",  # Title
        title_font=dict(
            size=20, family="Arial, sans-serif", color="navy"
        ),  # Title font settings
        paper_bgcolor="rgba(0,0,0,0.1)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        legend=dict(
            # Semi-transparent legend background
            bgcolor="rgba(255, 255, 255, 0.6)",
            bordercolor="Black",
            borderwidth=2,
        ),
        autosize=True,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fresh_water_details_input_reject_product_bar = fresh_water_details_charts()

    context = {
        "graph_json": graph_json,
        "total_input_water": total_input_water,
        "borewell_volume": borewell_volume,
        "tanker_volume": tanker_volume,
        "metro_volume": metro_volume,
        "rain_volume": rain_volume,
        "others_volume": others_volume,
        "fresh_water_details_input_reject_product_bar": fresh_water_details_input_reject_product_bar,
    }

    return render(request, "water_chart.html", context)


def get_source_water(user):
    sources = SourceWaterProfile.objects.filter(user=user)
    # Manual construction of data to include get_source_name_display
    sources_data = [
        {
            "id": source.id,
            "name": source.get_source_name_display(),
            "consumption": source.source_daily_consumption,
        }
        for source in sources
    ]

    # Serialize the manually constructed list of dictionaries to JSON
    return json.dumps(sources_data)


def get_freshwater_treatment(user):
    treatments = FreshWaterTreatmentProfile.objects.filter(user=user)
    treatments_data = [
        {
            "id": treatment.id,
            "name": treatment.name,
            "seq_number": treatment.id,
            "input_water": str(treatment.details.input_water),
            "product_water": str(treatment.details.product_water),
            "reject_water": str(treatment.details.reject_water),
        }
        for treatment in treatments
    ]

    return json.dumps(treatments_data)

from rest_framework import serializers

class SourceWaterFlowSerializer(serializers.ModelSerializer):
    node_type = serializers.SerializerMethodField()
    reject_water = serializers.SerializerMethodField()

    class Meta:
        model = SourceWaterFlow
        fields = ['source', 'destination', 'volume', 'node_type', 'reject_water']

    def get_node_type(self, obj):
        # Logic to determine node type based on your specific criteria
        if "tank" in obj.destination.lower():
            return 'tankNode'
        elif any(meth.name in obj.destination for meth in FreshWaterTreatmentMethods.objects.all()):
            return 'treatmentNode'
        return 'sourceNode'

    def get_reject_water(self, obj):
        # Fetch reject water information if it's a treatment process
        details = FreshWaterTreatmentProfileDetails.objects.filter(profile__name=obj.destination).first()
        return details.reject_water if details else None


@login_required
def flowchart_view(request):
    user = request.user
    source_water_flow_data = SourceWaterFlow.objects.filter(user=user).all()
    source_water_flow_json = serialize('json', source_water_flow_data)

    context = {
        "source_water_flow": source_water_flow_json,
    }
    return render(request, "flowchart.html", context)


@login_required
def tanks_capacities(request):
    tank_names = ['Input freshwater tank',
                'Fire tank',
                'Softener Storage tank',
                'RO Storage tank',
                'Flush tank',
                'Domestic Water tank',
                'RO Input tank',
                'Boiler Makeup tank',
                'Others']
    current_user = request.user
    if request.method == "POST":
        form = TanksCapacitiesForm(request.POST)
        if form.is_valid():
            form.instance.user = current_user
            names = request.POST.getlist('name')
            capacities = request.POST.getlist('capacity')
            other_tank_name = request.POST.getlist('tank_name')
            print(other_tank_name)
            if names and capacities:
                for i in range(len(names)):
                    if capacities[i]:  # Check if capacity is non-empty
                        if names[i] == 'Others':
                            tank_capacity = TanksCapacities.objects.create(user=current_user, name=other_tank_name[0], capacity=capacities[i])
                            other_tank_name = other_tank_name[1:]
                        else:
                            tank_capacity = TanksCapacities.objects.create(user=current_user, name=names[i], capacity=capacities[i])
                        tank_capacity.save()
            return redirect("tanks_capacities")
        else:
            print(form.errors)
    else:
        form = TanksCapacitiesForm()

    all_tanks = TanksCapacities.objects.filter(user=request.user)
    return render(
        request, "TanksCapacities.html", {"form": form, "all_tanks": all_tanks, 'tank_names': tank_names}
    )


@login_required
def delete_tanks_capacities(request):
    current_user = request.user
    TanksCapacities.objects.filter(user=current_user).delete()
    return redirect("tanks_capacities")





@login_required
def source_water_flow(request):
    existing_entries = SourceWaterFlow.objects.filter(user=request.user).exists()
    extra_forms = 0 if existing_entries else 1

    SourceWaterFlowFormSet = modelformset_factory(SourceWaterFlow, form=SourceWaterFlowForm, extra=extra_forms, can_delete=True)

    # Fetching all sources and destinations from the database
    fresh_water_sources = SourceWaterProfile.objects.filter(user=request.user)
    treatment_methods = FreshWaterTreatmentProfile.objects.filter(user=request.user)
    tanks = TanksCapacities.objects.filter(user=request.user)

    sources = [(source.source_name, source.source_name) for source in fresh_water_sources] + \
              [(method.name, method.name) for method in treatment_methods] + \
              [(tank.name, tank.name) for tank in tanks]

    destinations = [(method.name, method.name) for method in treatment_methods] + \
                   [(tank.name, tank.name) for tank in tanks]

    if 'reset' in request.POST:
        SourceWaterFlow.objects.filter(user=request.user).delete()
        existing_entries = False
        return redirect('source_water_flow')

    if request.method == "POST" and not existing_entries:
        formset = SourceWaterFlowFormSet(
            request.POST,
            request.FILES,
            queryset=SourceWaterFlow.objects.none(),
            form_kwargs={'sources': sources, 'destinations': destinations}
        )
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.source and instance.destination and instance.volume:
                    instance.user = request.user
                    instance.save()
            existing_entries = True
            return redirect('source_water_flow')

    formset = SourceWaterFlowFormSet(
        queryset=SourceWaterFlow.objects.filter(user=request.user) if existing_entries else SourceWaterFlow.objects.none(),
        form_kwargs={'sources': sources, 'destinations': destinations}
    )
    return render(request, "SourceWaterFlow.html", {
        'formset': formset,
        'existing_entries': existing_entries
    })






@login_required
def delete_source_water_flow(request):
    current_user = request.user
    SourceWaterFlow.objects.filter(user=current_user).delete()
    return redirect('source-destination')


@login_required
def kitchen_consumption_view(request):
    current_user = request.user
    all_details = KitchenDishwasherTapConsumption.objects.filter(user=current_user)
    details = KitchenDishwasherTapConsumption.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = KitchenDishwasherTapConsumptionForm(request.POST)
        if form.is_valid():
            kitchen_consumption = form.save()
            kitchen_consumption.user = request.user
            kitchen_consumption.save()
            return redirect("kitchen_consumption")
    else:
        form = KitchenDishwasherTapConsumptionForm()
    return render(
        request,
        "KitchenConsumption.html",
        {
        "form": form, 
        # "details": details,
         "all_details": all_details}
        ,
    )


@login_required
def delete_kitchen_consumption(request):
    current_user = request.user
    KitchenDishwasherTapConsumption.objects.filter(user=current_user).delete()
    return redirect("kitchen_consumption")


@login_required
def delete_kitchen(request, kitchen_id):
    # Get the restaurant object to delete
    kitchen = get_object_or_404(KitchenDishwasherTapConsumption, id=kitchen_id)
    # Delete the restaurant
    kitchen.delete()

    return redirect("kitchen_consumption")


@login_required
def drinking_water_source_view(request):
    current_user = request.user
    details = DrinkingWaterSource.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = DrinkingWaterSourceForm(request.POST)
        if form.is_valid():
            drinking_water = form.save(commit=False)
            drinking_water.user = current_user
            drinking_water.save()

            source_names = form.cleaned_data['source_name']
            for name in source_names:
                name = name.strip()
                if name:
                    source, created = DrinkingWaterSystem.objects.get_or_create(name=name)
                    drinking_water.source_name.add(source)

            source_names = request.POST.getlist('other_sources')
            sources = request.POST.getlist('source')
            if source_names:
                for name in source_names:
                    source, created = DrinkingWaterSystem.objects.get_or_create(name=name.strip())
                    drinking_water.source_name.add(source)

            if sources:
                for name in sources:
                    water_source, created1 = DrinkingWaterSourceName.objects.get_or_create(name=name.strip()) 
                    drinking_water.source.add(water_source)                 

            messages.success(request, "Drinking water source data saved successfully!")
            return redirect("guestroom_consumption")
    else:
        if details:
            form = DrinkingWaterSourceForm(instance=details)
        else:
            form = DrinkingWaterSourceForm()

    drinking_object = DrinkingWaterSource.objects.filter(user=current_user).first()
    sources = []
    water_sources = []
    if drinking_object:
        sources = drinking_object.source_name.all() 
        water_sources = drinking_object.source.all()  

    return render(
        request, "DrinkingWaterSource.html", {"form": form, "details": details, 'sources': sources, 'water_sources': water_sources}
    )


@login_required
def delete_drinking_water_source(request):
    current_user = request.user
    DrinkingWaterSource.objects.filter(user=current_user).delete()
    return redirect("drinking_water_source")


@login_required
def restaurant_consumption_view(request):
    current_user = request.user
    details = RestaurantConsumption.objects.filter(user=current_user).first()
    all_details = RestaurantConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = RestaurantConsumptionForm(request.POST)
        if form.is_valid():
            restaurant_consumption = form.save(commit=False)
            restaurant_consumption.user = current_user
            restaurant_consumption.save()
            messages.success(request, "Restaurant consumption data saved successfully!")
            return redirect("restaurant_consumption")
    else:
        form = RestaurantConsumptionForm()
    return render(
        request,
        "RestaurantConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
    )


@login_required
def delete_restaurant_consumption(request):
    current_user = request.user
    RestaurantConsumption.objects.filter(user=current_user).delete()
    return redirect("restaurant_consumption")


@login_required
def delete_restaurant(request, restaurant_id):
    # Get the restaurant object to delete
    restaurant = get_object_or_404(RestaurantConsumption, id=restaurant_id)
    # Delete the restaurant
    restaurant.delete()

    return redirect("restaurant_consumption")


@login_required
def banquet_consumption_view(request):
    current_user = request.user
    details = BanquetConsumption.objects.filter(user=current_user).first()
    all_details = BanquetConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = BanquetConsumptionForm(request.POST)
        if form.is_valid():
            banquet_consumption = form.save(commit=False)
            banquet_consumption.user = current_user
            banquet_consumption.save()

            other_sources = form.cleaned_data['drinking_water_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = BanquetSource.objects.get_or_create(name=name)
                    banquet_consumption.drinking_water_source.add(source)

            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:
                    source, created = BanquetSource.objects.get_or_create(name=name.strip())
                    banquet_consumption.drinking_water_source.add(source)  

            messages.success(request, "Banquet consumption data saved successfully!")
            return redirect("banquet_consumption")
    else:
        form = BanquetConsumptionForm()

    banquet_object = BanquetConsumption.objects.filter(user=current_user).first()
    sources = []
    if banquet_object:
        sources = banquet_object.drinking_water_source.all()

    return render(
        request,
        "BanquetConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_banquet_consumption(request):
    current_user = request.user
    BanquetConsumption.objects.filter(user=current_user).delete()
    return redirect("banquet_consumption")


@login_required
def delete_banquet(request, banquet_id):
    # Get the restaurant object to delete
    banquet = get_object_or_404(BanquetConsumption, id=banquet_id)
    # Delete the restaurant
    banquet.delete()

    return redirect("banquet_consumption")


@login_required
def guestroom_consumption_view(request):
    current_user = request.user
    details = GuestRoomConsumption.objects.filter(user=current_user).first()
    all_details = GuestRoomConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = GuestRoomConsumptionForm(request.POST)
        if form.is_valid():
            guestroom_consumption = form.save(commit=False)
            guestroom_consumption.user = current_user
            guestroom_consumption.save()

            other_domestic_sources = form.cleaned_data['domestic_flushing_source']
            other_toilet_sources = form.cleaned_data['toilet_flushing_source']
            for name in other_domestic_sources:
                name = name.strip()
                if name:
                    domestic_source, created = GuestRoomDomesticSource.objects.get_or_create(name=name)
                    guestroom_consumption.domestic_flushing_source.add(domestic_source)

            for name in other_toilet_sources:
                name = name.strip()
                if name:
                    toilet_source, created = GuestRoomToiletSource.objects.get_or_create(name=name)
                    guestroom_consumption.toilet_flushing_source.add(toilet_source)   

            other_domestic_sources = request.POST.getlist('other_domestic_sources')
            other_toilet_sources = request.POST.getlist('other_toilet_sources')

            if other_domestic_sources:
                for name in other_domestic_sources:
                    domestic_source, created = GuestRoomDomesticSource.objects.get_or_create(name=name.strip())
                    guestroom_consumption.domestic_flushing_source.add(domestic_source) 

            if other_toilet_sources:
                for name in other_toilet_sources:
                    toilet_source, created = GuestRoomToiletSource.objects.get_or_create(name=name.strip())
                    guestroom_consumption.toilet_flushing_source.add(toilet_source)

            messages.success(request, "Guest Room consumption data saved successfully!")
            return redirect("guestroom_consumption")
    else:
        form = GuestRoomConsumptionForm()

    guestroom_object = GuestRoomConsumption.objects.filter(user=current_user).first()
    domestic_sources = []
    toilet_sources = []
    if guestroom_object:
        domestic_sources = guestroom_object.domestic_flushing_source.all()
        toilet_sources = guestroom_object.toilet_flushing_source.all()

    return render(
        request,
        "GuestRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'domestic_sources': domestic_sources, 'toilet_sources': toilet_sources},
    )


@login_required
def delete_guestroom_consumption(request):
    current_user = request.user
    GuestRoomConsumption.objects.filter(user=current_user).delete()
    return redirect("guestroom_consumption")


@login_required
def delete_guestroom(request, guestroom_id):
    # Get the restaurant object to delete
    guestroom = get_object_or_404(GuestRoomConsumption, id=guestroom_id)
    # Delete the restaurant
    guestroom.delete()

    return redirect("guestroom_consumption")


@login_required
def employeeroom_consumption_view(request):
    current_user = request.user
    details = EmployeeRoomConsumption.objects.filter(user=current_user).first()
    all_details = EmployeeRoomConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = EmployeeRoomConsumptionForm(request.POST)
        if form.is_valid():
            employeeroom_consumption = form.save(commit=False)
            employeeroom_consumption.user = current_user
            employeeroom_consumption.save()

            other_domestic_sources = form.cleaned_data['domestic_flushing_source']
            other_toilet_sources = form.cleaned_data['toilet_flushing_source']
            for name in other_domestic_sources:
                name = name.strip()
                if name:
                    domestic_source, created = EmployeeRoomDomesticSource.objects.get_or_create(name=name)
                    employeeroom_consumption.domestic_flushing_source.add(domestic_source)

            for name in other_toilet_sources:
                name = name.strip()
                if name:
                    toilet_source, created = EmployeeRoomToiletSource.objects.get_or_create(name=name)
                    employeeroom_consumption.toilet_flushing_source.add(toilet_source)   

            other_domestic_sources = request.POST.getlist('other_domestic_sources')
            other_toilet_sources = request.POST.getlist('other_toilet_sources')

            if other_domestic_sources:
                for name in other_domestic_sources:
                    domestic_source, created = EmployeeRoomDomesticSource.objects.get_or_create(name=name.strip())
                    employeeroom_consumption.domestic_flushing_source.add(domestic_source) 

            if other_toilet_sources:
                for name in other_toilet_sources:
                    toilet_source, created = EmployeeRoomToiletSource.objects.get_or_create(name=name.strip())
                    employeeroom_consumption.toilet_flushing_source.add(toilet_source)
                    
            return redirect("employeeroom_consumption")
    else:
        form = EmployeeRoomConsumptionForm()

    employeeroom_object = EmployeeRoomConsumption.objects.filter(user=current_user).first()
    domestic_sources = []
    toilet_sources = []
    if employeeroom_object:
        domestic_sources = employeeroom_object.domestic_flushing_source.all()
        toilet_sources = employeeroom_object.toilet_flushing_source.all()

    return render(
        request,
        "EmployeeRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'domestic_sources': domestic_sources, 'toilet_sources': toilet_sources},
    )


@login_required
def delete_employeeroom_consumption(request):
    current_user = request.user
    EmployeeRoomConsumption.objects.filter(user=current_user).delete()
    return redirect("employeeroom_consumption")


@login_required
def delete_employeeroom(request, employeeroom_id):
    # Get the restaurant object to delete
    employeeroom = get_object_or_404(EmployeeRoomConsumption, id=employeeroom_id)
    # Delete the restaurant
    employeeroom.delete()

    return redirect("employeeroom_consumption")


@login_required
def driversroom_consumption_view(request):
    current_user = request.user
    details = DriversRoomConsumption.objects.filter(user=current_user).first()
    all_details = DriversRoomConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = DriversRoomConsumptionForm(request.POST)
        if form.is_valid():
            driversroom_consumption = form.save(commit=False)
            driversroom_consumption.user = current_user
            driversroom_consumption.save()
            # if driversroom_consumption.other_source_name:
            #     driversroom_consumption.drivers_room_source = driversroom_consumption.other_source_name
            other_domestic_sources = form.cleaned_data['domestic_flushing_source']
            other_toilet_sources = form.cleaned_data['toilet_flushing_source']
            for name in other_domestic_sources:
                name = name.strip()
                if name:
                    domestic_source, created = DriversRoomDomesticSource.objects.get_or_create(name=name)
                    driversroom_consumption.domestic_flushing_source.add(domestic_source)

            for name in other_toilet_sources:
                name = name.strip()
                if name:
                    toilet_source, created = DriversRoomToiletSource.objects.get_or_create(name=name)
                    driversroom_consumption.toilet_flushing_source.add(toilet_source)   

            other_domestic_sources = request.POST.getlist('other_domestic_sources')
            other_toilet_sources = request.POST.getlist('other_toilet_sources')

            if other_domestic_sources:
                for name in other_domestic_sources:
                    domestic_source, created = DriversRoomDomesticSource.objects.get_or_create(name=name.strip())
                    driversroom_consumption.domestic_flushing_source.add(domestic_source) 

            if other_toilet_sources:
                for name in other_toilet_sources:
                    toilet_source, created = DriversRoomToiletSource.objects.get_or_create(name=name.strip())
                    driversroom_consumption.toilet_flushing_source.add(toilet_source)

            return redirect("driversroom_consumption")
    else:
        form = DriversRoomConsumptionForm()

    driversroom_object = DriversRoomConsumption.objects.filter(user=current_user).first()
    domestic_sources = []
    toilet_sources = []
    if driversroom_object:
        domestic_sources = driversroom_object.domestic_flushing_source.all()
        toilet_sources = driversroom_object.toilet_flushing_source.all()

    return render(
        request,
        "DriversRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'domestic_sources': domestic_sources, 'toilet_sources': toilet_sources},
    )


@login_required
def delete_driversroom_consumption(request):
    current_user = request.user
    DriversRoomConsumption.objects.filter(user=current_user).delete()
    return redirect("driversroom_consumption")


@login_required
def delete_driversroom(request, driversroom_id):
    # Get the restaurant object to delete
    driversroom = get_object_or_404(DriversRoomConsumption, id=driversroom_id)
    # Delete the restaurant
    driversroom.delete()

    return redirect("driversroom_consumption")


@login_required
def swimmingpool_consumption_view(request):
    # sourcery skip: merge-else-if-into-elif, use-named-expression
    current_user = request.user
    details = SwimmingPoolConsumption.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = SwimmingPoolConsumptionForm(request.POST)
        if form.is_valid():
            swimmingpool_consumption = form.save(commit=False)
            swimmingpool_consumption.user = current_user
            swimmingpool_consumption.save()
            
            other_sources = form.cleaned_data['swimming_pool_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = SwimmingPoolSource.objects.get_or_create(name=name)
                    swimmingpool_consumption.swimming_pool_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = SwimmingPoolSource.objects.get_or_create(name=name.strip())
                    swimmingpool_consumption.swimming_pool_source.add(source)
                
            return redirect("waterbodies_consumption")
        else:
            print(form.errors)
    else:
        if details:
            form = SwimmingPoolConsumptionForm(instance=details)
        else:
            form = SwimmingPoolConsumptionForm()
            
    swimming_object = SwimmingPoolConsumption.objects.filter(user=current_user).first()
    sources = []
    if swimming_object:
        sources = swimming_object.swimming_pool_source.all()
    
    return render(
        request, "SwimmingPoolConsumption.html", {"form": form, "details": details, "sources": sources}
    )
# for source in SwimmingPoolConsumption.objects.all():
#     print(source.swimming_pool_source.all())


@login_required
def delete_swimmingpool_consumption(request):
    current_user = request.user
    SwimmingPoolConsumption.objects.filter(user=current_user).delete()
    return redirect("swimmingpool_consumption")


@login_required
def waterbodies_consumption_view(request):
    current_user = request.user
    details = WaterBodiesConsumption.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = WaterBodiesConsumptionForm(request.POST)
        if form.is_valid():
            waterbody_consumption = form.save(commit=False)
            waterbody_consumption.user = current_user
            waterbody_consumption.save()

            other_sources = form.cleaned_data['water_body_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = WaterBodiesSource.objects.get_or_create(name=name)
                    waterbody_consumption.water_body_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = WaterBodiesSource.objects.get_or_create(name=name.strip())
                    waterbody_consumption.water_body_source.add(source)
            return redirect("laundry_consumption")
        else:
            print(form.errors)
    else:
        if details:
            form = WaterBodiesConsumptionForm(instance=details)
        else:
            form = WaterBodiesConsumptionForm()

    waterbody_object = WaterBodiesConsumption.objects.filter(user=current_user).first()
    sources = []
    if waterbody_object:
        sources = waterbody_object.water_body_source.all()

    return render(
        request, "WaterBodiesConsumption.html", {"form": form, "details": details, 'sources': sources}
    )


@login_required
def delete_waterbodies_consumption(request):
    current_user = request.user
    WaterBodiesConsumption.objects.filter(user=current_user).delete()
    return redirect('waterbodies_consumption')



@login_required
def source_dash_view(request):
    user_dash_app = create_user_dash_app(request.user)
    sources = SourceWaterProfile.objects.filter(user=request.user).all()
    return render(request, "DashSource.html")


def laundry_consumption_view(request):
    current_user = request.user
    details = LaundryConsumption.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = LaundryConsumptionForm(request.POST)
        if form.is_valid():
            laundry_consumption = form.save(commit=False)
            laundry_consumption.user = current_user
            laundry_consumption.save()

            other_sources = form.cleaned_data['laundry_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = LaundrySource.objects.get_or_create(name=name)
                    laundry_consumption.laundry_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = LaundrySource.objects.get_or_create(name=name.strip())
                    laundry_consumption.laundry_source.add(source)
            return redirect("boiler_consumption")
    else:
        if details:
            form = LaundryConsumptionForm(instance=details)
        else:
            form = LaundryConsumptionForm()

    laundry_object = LaundryConsumption.objects.filter(user=current_user).first()
    sources = []
    if laundry_object:
        sources = laundry_object.laundry_source.all()

    return render(
        request, "LaundryConsumption.html", {"form": form, "details": details, 'sources': sources}
    )


@login_required
def delete_laundry_consumption(request):
    current_user = request.user
    LaundryConsumption.objects.filter(user=current_user).delete()
    return redirect("laundry_consumption")


@login_required
def boiler_consumption_view(request):
    current_user = request.user
    consumption_details = BoilerConsumption.objects.filter(user=current_user).first()
    all_details = BoilerConsumption.objects.filter(user=current_user)
    all_treatment_methods = BoilerTreatmentMethods.objects.filter(user=request.user)

    if request.method == "POST":
        consumption_form = BoilerConsumptionForm(request.POST, prefix="consumption")

        if consumption_form.is_valid():
            consumption = consumption_form.save(commit=False)
            consumption.user = current_user
            consumption.save()

            other_sources = consumption_form.cleaned_data['boiler_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = BoilerSource.objects.get_or_create(name=name)
                    consumption.boiler_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = BoilerSource.objects.get_or_create(name=name.strip())
                    consumption.boiler_source.add(source)
                    
            pre_treatment = consumption_form.cleaned_data.get("pre_treatment_boiler")
            if pre_treatment == "2":
                return redirect("boiler_treatment_method")
            else:
                return redirect("add_boiler")
    else:
        if consumption_details:
            consumption_form = BoilerConsumptionForm(
                instance=consumption_details, prefix="consumption"
            )
        else:
            consumption_form = BoilerConsumptionForm(prefix="consumption")

    boiler_object = BoilerConsumption.objects.filter(user=current_user).first()
    sources = []
    if_steam = None
    if boiler_object:
        sources = boiler_object.boiler_source.all()        
        if_steam = boiler_object.steam_recovery

    return render(
        request,
        "BoilerConsumption.html",
        {
            "consumption_form": consumption_form,
            "details": consumption_details,
            "all_details": all_details,
            "all_treatment_methods": all_treatment_methods,
            "sources": sources,
            "if_steam" : if_steam
        },
    )


@login_required
def delete_boiler_consumption(request):
    current_user = request.user
    BoilerConsumption.objects.filter(user=current_user).delete()
    BoilerTreatmentMethods.objects.filter(user=current_user).delete()
    return redirect("boiler_consumption")


@login_required
def boiler_treatment_methods_view(request):
    current_user = request.user
    all_treatment_methods = BoilerTreatmentMethods.objects.filter(user=request.user)

    if request.method == "POST":
        treatment_form = BoilerTreatmentMethodsForm(request.POST, prefix="treatment")
        if treatment_form.is_valid():
            treatment = treatment_form.save(commit=False)
            treatment.user = current_user
            treatment.save()
            return redirect("boiler_treatment_method")
    else:
        treatment_form = BoilerTreatmentMethodsForm(prefix="treatment")

    return render(
        request,
        "BoilerTreatmentMethod.html",
        {
            "treatment_form": treatment_form,
            "all_treatment_methods": all_treatment_methods,
        },
    )


@login_required
def delete_boiler_treatment_method(request, boiler_treatment_id):
    # Get the restaurant object to delete
    boiler_treatment = get_object_or_404(BoilerTreatmentMethods, id=boiler_treatment_id)
    # Delete the restaurant
    boiler_treatment.delete()

    return redirect("boiler_treatment_method")


@login_required
def add_boiler_view(request):
    current_user = request.user
    details = AddBoilerConsumption.objects.filter(user=current_user).first()
    all_details = AddBoilerConsumption.objects.filter(user=current_user)
    all_treatment_methods = BoilerTreatmentMethods.objects.filter(user=request.user)

    if request.method == "POST":
        form = AddBoilerConsumptionForm(request.POST)
        if form.is_valid():
            add_boiler = form.save(commit=False)
            add_boiler.user = current_user
            add_boiler.save()
            return redirect("add_boiler")
    else:
        form = AddBoilerConsumptionForm()
    return render(
        request,
        "AddBoilerConsumption.html",
        {
            "form": form,
            "details": details,
            "all_details": all_details,
            "all_treatment_methods": all_treatment_methods,
        },
    )


@login_required
def delete_each_boiler_consumption(request):
    current_user = request.user
    AddBoilerConsumption.objects.filter(user=current_user).delete()
    return redirect("add_boiler")


@login_required
def delete_each_boiler(request, boiler_id):
    # Get the boiler object to delete
    boiler = get_object_or_404(AddBoilerConsumption, id=boiler_id)
    # Delete the boiler
    boiler.delete()

    return redirect("add_boiler")


@login_required
def calorifier_consumption_view(request):
    current_user = request.user
    details = CalorifierConsumption.objects.filter(user=current_user).first()
    all_details = CalorifierConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = CalorifierConsumptionForm(request.POST)
        if form.is_valid():
            calorifier = form.save(commit=False)
            calorifier.user = current_user
            calorifier.save()

            other_sources = form.cleaned_data['calorifier_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = CalorifierSource.objects.get_or_create(name=name)
                    calorifier.calorifier_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = CalorifierSource.objects.get_or_create(name=name.strip())
                    calorifier.calorifier_source.add(source)
        
            return redirect("calorifier_consumption")
    else:
        form = CalorifierConsumptionForm()

    calorifier_object = CalorifierConsumption.objects.filter(user=current_user).first()
    sources = []
    if calorifier_object:
        sources = calorifier_object.calorifier_source.all()

    return render(
        request,
        "CalorifierConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_calorifier_consumption(request):
    current_user = request.user
    CalorifierConsumption.objects.filter(user=current_user).delete()
    return redirect("calorifier_consumption")


@login_required
def delete_calorifier(request, calorifier_id):
    # Get the boiler object to delete
    calorifier = get_object_or_404(CalorifierConsumption, id=calorifier_id)
    # Delete the boiler
    calorifier.delete()

    return redirect("calorifier_consumption")


@login_required
def coolingtower_consumption_view(request):
    current_user = request.user
    details = CoolingTowerConsumption.objects.filter(user=current_user).first()
    all_details = CoolingTowerConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = CoolingTowerConsumptionForm(request.POST)

        if form.is_valid():
            cooling_tower = form.save(commit=False)
            cooling_tower.user = current_user
            cooling_tower.save()
            return redirect("add_coolingtower")
    else:
        if details:
            form = CoolingTowerConsumptionForm(instance=details)
        else:
            form = CoolingTowerConsumptionForm()

    return render(
        request,
        "CoolingTowerConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
    )


@login_required
def delete_coolingtower_consumption(request):
    current_user = request.user
    CoolingTowerConsumption.objects.filter(user=current_user).delete()
    return redirect("coolingtower_consumption")


@login_required
def add_coolingtower_view(request):
    current_user = request.user
    details = AddCoolingTowerConsumption.objects.filter(user=current_user).first()
    all_details = AddCoolingTowerConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = AddCoolingTowerConsumptionForm(request.POST)
        if form.is_valid():
            add_coolingtower = form.save(commit=False)
            add_coolingtower.user = current_user
            add_coolingtower.save()

            other_sources = form.cleaned_data['cooling_tower_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = AddCoolingTowerSource.objects.get_or_create(name=name)
                    add_coolingtower.cooling_tower_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = AddCoolingTowerSource.objects.get_or_create(name=name.strip())
                    add_coolingtower.cooling_tower_source.add(source)

            return redirect("add_coolingtower")
    else:
        form = AddCoolingTowerConsumptionForm()

    addCoolingTower_object = AddCoolingTowerConsumption.objects.filter(user=current_user).first()
    sources = []
    if addCoolingTower_object:
        sources = addCoolingTower_object.cooling_tower_source.all()

    return render(
        request,
        "AddCoolingTowerConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_each_coolingtower_consumption(request):
    current_user = request.user
    AddCoolingTowerConsumption.objects.filter(user=current_user).delete()
    return redirect("add_coolingtower")


@login_required
def delete_each_coolingtower(request, coolingtower_id):
    # Get the boiler object to delete
    coolingtower = get_object_or_404(AddCoolingTowerConsumption, id=coolingtower_id)
    # Delete the boiler
    coolingtower.delete()

    return redirect("add_coolingtower")


@login_required
def irrigation_consumption_view(request):
    current_user = request.user
    details = IrrigationConsumption.objects.filter(user=current_user).first()
    all_details = IrrigationConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = IrrigationConsumptionForm(request.POST)

        if form.is_valid():
            irrigation = form.save(commit=False)
            irrigation.user = current_user
            irrigation.save()

            other_sources = form.cleaned_data['irrigation_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = IrrigationSource.objects.get_or_create(name=name)
                    irrigation.irrigation_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = IrrigationSource.objects.get_or_create(name=name.strip())
                    irrigation.irrigation_source.add(source)
            return redirect("other_consumption")
    else:
        if details:
            form = IrrigationConsumptionForm(instance=details)
        else:
            form = IrrigationConsumptionForm()

    irrigation_object = IrrigationConsumption.objects.filter(user=current_user).first()
    sources = []
    if irrigation_object:
        sources = irrigation_object.irrigation_source.all()        

    return render(
        request,
        "IrrigationConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_irrigation_consumption(request):
    current_user = request.user
    IrrigationConsumption.objects.filter(user=current_user).delete()
    return redirect("irrigation_consumption")


@login_required
def other_consumption_view(request):
    current_user = request.user
    details = OtherConsumption.objects.filter(user=current_user).first()
    all_details = OtherConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = OtherConsumptionForm(request.POST)

        if form.is_valid():
            other_consumption = form.save(commit=False)
            other_consumption.user = current_user
            other_consumption.save()

            other_sources = form.cleaned_data['other_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = OtherConsumptionSource.objects.get_or_create(name=name)
                    other_consumption.other_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = OtherConsumptionSource.objects.get_or_create(name=name.strip())
                    other_consumption.other_source.add(source)
            return redirect("wastewater_treatment")
    else:
        if details:
            form = OtherConsumptionForm(instance=details)
        else:
            form = OtherConsumptionForm()

    other_consumption_object = OtherConsumption.objects.filter(user=current_user).first()
    sources = []
    if other_consumption_object:
        sources = other_consumption_object.other_source.all()        

    return render(
        request,
        "OtherConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_other_consumption(request):
    current_user = request.user
    OtherConsumption.objects.filter(user=current_user).delete()
    return redirect("other_consumption")


@login_required
def wastewater_treatment_view(request):
    current_user = request.user
    details = WasteWaterTreatment.objects.filter(user=current_user).first()
    # details1 = WasteWaterTreatmentSTP.objects.filter(user=current_user).first()
    # details2 = WasteWaterTreatmentETP.objects.filter(user=current_user).first()
    # details3 = WasteWaterTreatmentOthers.objects.filter(user=current_user).first()

    if request.method == "POST":
        form = WasteWaterTreatmentForm(request.POST)

        if form.is_valid():
            waste_water = form.save(commit=False)
            waste_water.user = current_user
            waste_water.save()
            if form.cleaned_data.get("treatment_method") == "STP":
                return redirect("wastewater_treatment_STP")
            elif form.cleaned_data.get("treatment_method") == "ETP":
                return redirect("wastewater_treatment_ETP")
            else:
                return redirect("wastewater_treatment_Others")
    else:
        if details:
            form = WasteWaterTreatmentForm(instance=details)
        else:
            form = WasteWaterTreatmentForm()

    return render(
        request, "WasteWaterTreatment.html", {"form": form, "details": details}
    )


@login_required
def delete_wastewater_treatment(request):
    current_user = request.user
    WasteWaterTreatment.objects.filter(user=current_user).delete()
    WasteWaterTreatmentSTP.objects.filter(user=current_user).delete()
    WasteWaterTreatmentETP.objects.filter(user=current_user).delete()
    WasteWaterTreatmentOthers.objects.filter(user=current_user).delete()
    return redirect("wastewater_treatment")


@login_required
def wastewater_treatment_STP_view(request):
    current_user = request.user
    details = WasteWaterTreatmentSTP.objects.filter(user=current_user).first()

    if request.method == "POST":
        form = WasteWaterTreatmentSTPForm(request.POST)

        if form.is_valid():
            wastewater_treatment_STP = form.save(commit=False)
            wastewater_treatment_STP.user = current_user
            wastewater_treatment_STP.save()
            return redirect("tanks_and_capacities")
    else:
        if details:
            form = WasteWaterTreatmentSTPForm(instance=details)
        else:
            form = WasteWaterTreatmentSTPForm()

    return render(
        request, "WasteWaterTreatmentSTP.html", {"form": form, "details": details}
    )


@login_required
def delete_wastewater_treatment_STP(request):
    current_user = request.user
    WasteWaterTreatmentSTP.objects.filter(user=current_user).delete()
    return redirect("wastewater_treatment_STP")


@login_required
def wastewater_treatment_ETP_view(request):
    current_user = request.user
    details = WasteWaterTreatmentETP.objects.filter(user=current_user).first()

    if request.method == "POST":
        form = WasteWaterTreatmentETPForm(request.POST)

        if form.is_valid():
            wastewater_treatment_ETP = form.save(commit=False)
            wastewater_treatment_ETP.user = current_user
            wastewater_treatment_ETP.save()
            return redirect("tanks_and_capacities")
    else:
        if details:
            form = WasteWaterTreatmentETPForm(instance=details)
        else:
            form = WasteWaterTreatmentETPForm()

    return render(
        request, "WasteWaterTreatmentETP.html", {"form": form, "details": details}
    )


@login_required
def delete_wastewater_treatment_ETP(request):
    current_user = request.user
    WasteWaterTreatmentETP.objects.filter(user=current_user).delete()
    return redirect("wastewater_treatment_ETP")


@login_required
def wastewater_treatment_Others_view(request):
    current_user = request.user
    details = WasteWaterTreatmentOthers.objects.filter(user=current_user).first()

    if request.method == "POST":
        form = WasteWaterTreatmentOthersForm(request.POST)

        if form.is_valid():
            wastewater_treatment_Others = form.save(commit=False)
            wastewater_treatment_Others.user = current_user
            wastewater_treatment_Others.save()
            return redirect("tanks_and_capacities")
    else:
        if details:
            form = WasteWaterTreatmentOthersForm(instance=details)
        else:
            form = WasteWaterTreatmentOthersForm()

    return render(
        request, "WasteWaterTreatmentOthers.html", {"form": form, "details": details}
    )


@login_required
def delete_wastewater_treatment_Others(request):
    current_user = request.user
    WasteWaterTreatmentETP.objects.filter(user=current_user).delete()
    return redirect("wastewater_treatment_Others")


@login_required
def tanks_and_capacities_view(request):
    current_user = request.user
    details = TanksAndCapacities.objects.filter(user=current_user).first()
    water_treatment_details = WasteWaterTreatment.objects.filter(
        user=current_user
    ).first()

    if request.method == "POST":
        form = TanksAndCapacitiesForm(request.POST)

        if form.is_valid():
            tanks_and_capacities = form.save(commit=False)
            tanks_and_capacities.user = current_user
            tanks_and_capacities.save()

            other_sources = form.cleaned_data['tank_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = TanksAndCapacitiesSource.objects.get_or_create(name=name)
                    tanks_and_capacities.tank_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = SwimmingPoolSource.objects.get_or_create(name=name.strip())
                    tanks_and_capacities.tank_source.add(source)
            return redirect("water_quality_profile")
    else:
        if details:
            form = TanksAndCapacitiesForm(instance=details)
        else:
            form = TanksAndCapacitiesForm()

    tanksandcapacities_object = TanksAndCapacities.objects.filter(user=current_user).first()
    sources = []
    if tanksandcapacities_object:
        sources = tanksandcapacities_object.tank_source.all()
            

    return render(
        request,
        "TanksAndCapacities.html",
        {
            "form": form,
            "details": details,
            "water_treatment_details": water_treatment_details,
            "sources": sources
        },
    )


@login_required
def delete_tanks_and_capacities(request):
    current_user = request.user
    TanksAndCapacities.objects.filter(user=current_user).delete()
    return redirect("tanks_and_capacities")


@login_required
def water_quality_profile_view(request):
    current_user = request.user
    details = WaterQualityProfile.objects.filter(user=current_user).first()
    water_treatment_details = WasteWaterTreatment.objects.filter(
        user=current_user
    ).first()

    if request.method == "POST":
        form = WaterQualityProfileForm(request.POST)

        if form.is_valid():
            water_quality_profile = form.save(commit=False)
            water_quality_profile.user = current_user
            water_quality_profile.save()
            return redirect("thank_you")
    else:
        if details:
            form = WaterQualityProfileForm(instance=details)
        else:
            form = WaterQualityProfileForm()

    return render(
        request, 
        "WaterQualityProfile.html", 
        {"form": form, 
         "details": details,
         "water_treatment_details": water_treatment_details,
        },
    )


@login_required
def delete_water_quality_profile(request):
    current_user = request.user
    WaterQualityProfile.objects.filter(user=current_user).delete()
    return redirect("water_quality_profile")


@login_required
def recycled_water_view(request):
    current_user = request.user
    all_details = RecycledWaterProfile.objects.filter(user=current_user)
    details = RecycledWaterProfile.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = RecycledWaterProfileForm(request.POST)
        if form.is_valid():
            recycled_water = form.save(commit=False)
            recycled_water.user = request.user
            recycled_water.save()
            return redirect("recycled_water")
    else:
        form = RecycledWaterProfileForm()
    return render(
        request,
        "RecycledWater.html",
        {"form": form, "details": details, "all_details": all_details},
    )


@login_required
def delete_recycled_water_all(request):
    current_user = request.user
    RecycledWaterProfile.objects.filter(user=current_user).delete()
    return redirect("kitchen_consumption")


@login_required
def delete_recycled_water(request, recycled_water_id):
    # Get the restaurant object to delete
    recycled_water = get_object_or_404(RecycledWaterProfile, id=recycled_water_id)
    # Delete the restaurant
    recycled_water.delete()

    return redirect("recycled_water")


def show_map_view(request):
    return render(request, "rainfall_map.html")


# def generate_pdf_file():
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     doc.onFirstPage = lambda canvas, doc: canvas.setTitle("Digital Water Audit Report")

#     styles = getSampleStyleSheet()

#     # Custom styles
#     title_style = styles['Title'].clone('TitleStyle')
#     title_style.textColor = colors.darkblue
#     title_style.spaceAfter = 50
#     title_style.fontSize = 28

#     heading_style = styles['Heading1'].clone('HeadingStyle')
#     heading_style.spaceBefore = 10
#     heading_style.spaceAfter = 10
#     heading_style.leftIndent = 20


#     center_style = ParagraphStyle(name='Center', alignment=TA_CENTER)

#     # Title
#     elements = [Paragraph("Digital Water Audit Report", title_style)]

#     # Logo image
#     logo = "static/main_logo.png" 
#     logo_img = Image(logo, width=300, height=300)  # Set width and height as needed
#     logo_img.hAlign = 'CENTER'  
#     elements.append(logo_img)
#     elements.append(Spacer(1, 24))

#     # Description Text
#     description_text = "This report provides an detailed analysis of the water audit findings and insights."
#     elements.append(Paragraph(description_text, center_style))
    
#     elements.append(PageBreak())
    
#     # Index Page
    
#     elements.append(Paragraph("Index", title_style))
#     elements.append(Spacer(1, 24))
    
    

#     # List of sections
#     sections = [
#         "1. Introduction",
#         "2. Source Water Profile",
#         "3. Fresh Water Treatment Profile",
#         "4. Tanks and Capacities",
#         "5. Consumption Details",
#         "6. Waste Water Treatment",
#         "7. Water Quality Profile",
#         "8. Recycled Water Profile",
#         "9. Conclusion"
#     ]

#     for section in sections:
#         elements.append(Paragraph(section, heading_style))

#     doc.build(elements)

#     buffer.seek(0)
#     return buffer

# @login_required
# def generate_pdf(request):
#     pdf_content = generate_pdf_file()
#     response = FileResponse(pdf_content, filename='report.pdf')
#     response['Content-Disposition'] = 'inline; filename="report.pdf"'
#     return response




def initialize_styles():
    return getSampleStyleSheet()



def create_title_page(styles, user):
    user_details = get_object_or_404(BasicDetails, user=user)
    elements = []
    
    # Title setup with enhanced styling
    title_style = styles['Title'].clone('TitleStyle')
    title_style.textColor = colors.navy  # Subtle, professional color
    title_style.fontSize = 30  # Slightly smaller for elegance
    title_style.alignment = TA_CENTER
    title_paragraph = Paragraph("Digital Water Audit Report", title_style)
    elements.append(title_paragraph)
    elements.append(Spacer(1, 24))  # Adjusted for balance

    # Logo setup, centered and resized appropriately
    logo = "static/main_logo.png"
    logo_img = Image(logo, width=300, height=300)  # Smaller dimensions for balance
    logo_img.hAlign = 'CENTER'
    elements.append(logo_img)
    elements.append(Spacer(1, 20))

    # Description with justified alignment for clean text flow
    description_style = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=12)
    description_text = "This report provides a summary analysis of the water audit findings and insights."
    description_paragraph = Paragraph(description_text, description_style)
    elements.append(description_paragraph)
    # elements.append(Spacer(1, 20))

    elements.append(Spacer(1, 5))
    elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    # Contact information with left alignment and subtle indentations
    main_style = ParagraphStyle(name='main_style', alignment=TA_CENTER, leftIndent=10, rightIndent=50,
                                    spaceBefore=10, spaceAfter=10, fontSize=12)
    
    address_style = ParagraphStyle(name='address_style', alignment=TA_CENTER, leftIndent=10, rightIndent=50,
                                    spaceBefore=10, spaceAfter=10, fontSize=11, textColor=colors.grey)

    
    elements.append(Paragraph('<b> <font color="grey"> Water Audit at:</font> </b>', main_style))
    organization_name = f'<b> <font color="#00008B"> {user_details.organization_name} </font></b>'
    elements.append(Paragraph(organization_name, main_style))
    
    address = f"""
        {user_details.address}<br/><br/>
        Email: <font color="blue">{user_details.email_address}</font><br/>
        Phone: {user_details.contact_number}"""
    user_info = Paragraph(address, address_style)
    elements.append(user_info)

    elements.append(Spacer(1, 5))
    elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    
    elements.append(Paragraph('<b> <font color="grey"> Contact Us:</font> </b>', main_style))
    elements.append(Paragraph('<b> <font color="#00008B"> INTERNATIONAL CENTRE FOR CLEAN WATER </font> </b>', main_style))
    # Our organization information
    address = """
        2ND FLOOR, BLOCK – B, IIT MADRAS RESEARCH PARK,
        KANAGAM ROAD, TARAMANI, CHENNAI, TAMIL NADU - 600 113<br/><br/>
        Email: <font color="blue">nagarjuna@iccwindia.org</font><br/>
        Phone: +91 7676702164"""
    our_info = Paragraph(address, address_style)
    elements.append(our_info)
    elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
      # More space to ensure clean separation before page break
    elements.append(PageBreak())

    return elements


def create_index_page(styles):
    elements = []
    title_style = styles['Title'].clone('TitleStyle')
    title_style.fontSize = 30
    title_style.textColor = colors.navy
    heading_style = styles['Heading1'].clone('HeadingStyle')
    heading_style.spaceBefore = 10
    heading_style.spaceAfter = 10
    heading_style.leftIndent = 20
    heading_style.fontSize = 16
    # make heading style as hyperlink
    heading_style.textColor = colors.blue

    elements.append(Paragraph("Index", title_style))
    elements.append(Spacer(1, 24))
    elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    elements.append(Spacer(1, 24))
    exec_summary = '1. <u> <a href="#exec_sum">Executive Summary</a></u>'
    elements.append(Paragraph(exec_summary, heading_style))
    
    intro = '2. <u> <a href="#intro">Introduction</a></u>' 
    elements.append(Paragraph(intro, heading_style))
    
    source_water = '3. <u> <a href="#exec_sum">Source Water Profile</a></u>'
    elements.append(Paragraph(source_water, heading_style))
    
    fresh_water = '4. <u> <a href="#exec_sum">Fresh Water Treatment Profile</a></u>'
    elements.append(Paragraph(fresh_water, heading_style))
    
    consumption = '5. <u> <a href="#exec_sum">Consumption Details</a></u>'
    elements.append(Paragraph(consumption, heading_style))
    
    waste_water = '6. <u> <a href="#exec_sum">Waste Water Treatment</a></u>'
    elements.append(Paragraph(waste_water, heading_style))
    
    water_quality = '7. <u> <a href="#exec_sum">Water Quality Profile</a></u>'
    elements.append(Paragraph(water_quality, heading_style))
    
    water_saving = '8. <u> <a href="#exec_sum">Water Saving Solutions</a></u>'
    elements.append(Paragraph(water_saving, heading_style))
    
    conclusion = '9. <u> <a href="#exec_sum">Conclusion</a></u>'
    elements.append(Paragraph(conclusion, heading_style))
    

    elements.append(PageBreak())
    
    return elements


def create_executive_summary(styles, user):
    user_details = get_object_or_404(BasicDetails, user=user)
    elements = []

    # Title setup
    title_style = styles['Title'].clone('TitleStyle')
    title_style.fontSize = 22
    title_style.textColor = colors.navy
    title_style.alignment = TA_CENTER
    title_paragraph = Paragraph("<a name='exec_sum'/> Executive Summary", title_style)
    elements.append(title_paragraph)
    elements.append(Spacer(1, 18))
 
    # Executive summary content
    summary_style = styles['BodyText'].clone('SummaryStyle')
    summary_style.alignment = TA_JUSTIFY
    summary_style.fontSize = 12
    summary_style.spaceBefore = 6
    summary_style.spaceAfter = 6
    # add vertical space between lines
    summary_style.leading = 14
    summary_text = f"""
    The Digital Water Audit Report for <b>{user_details.organization_name}</b> summarizes the key findings, recommendations, and insights from the comprehensive water audit conducted at {user_details.address}. Key findings highlight areas of potential improvement, cost savings, and environmental benefits. Recommendations are intended to guide strategic decisions to enhance water efficiency and sustainability.
    """
    summary_paragraph = Paragraph(summary_text, summary_style)
    elements.append(summary_paragraph)
    elements.append(Spacer(1, 24))

    
    title_style = styles['Title'].clone('TitleStyle')
    title_style.fontSize = 18
    title_style.textColor = colors.olivedrab
    title_style.alignment = TA_LEFT
    title_paragraph = Paragraph("Organisation Details", title_style)
    elements.append(title_paragraph)
    
    
    # Organization details in a table
    table_data = [
        ['Organization Name', user_details.organization_name],
        ['Address', user_details.address],
        ['Contact Number', user_details.contact_number],
        ['Email Address', user_details.email_address],
        ['Organization Type', user_details.organization_type],
        ['Number of Permanent Employees', user_details.num_permanent_employees],
        ['Number of Temporary Employees', user_details.num_temporary_employees],
        ['Number of Rooms', user_details.num_rooms],
        ['Average Occupancy per Year', user_details.average_occupancy],
        ['Total Area (sq ft)', user_details.total_area],
        ['Built-Up Area (sq ft)', user_details.total_built_up_area],
        ['Green Area (sq ft)', user_details.total_green_area],
        ['Air-Conditioned Space (sq ft)', user_details.total_air_conditioned_space_area]
    ]

    table = Table(table_data, colWidths=[200, 280], spaceBefore=20, spaceAfter=20)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        # ('GRID', (0, 0), (-1, -1), 1, colors.gray),

    ])
    table.setStyle(table_style)
    elements.append(table)

    elements.append(PageBreak())
    
    title_paragraph = Paragraph("Rationale For WATER AUDIT", title_style)
    elements.append(title_paragraph)
    elements.append(Spacer(1, 18))
    
    
    summary_text = f"""
    Water audit determines the amount of water lost from the water network/distribution system due to seepage, evaporation/leakage and other reasons such as theft, unauthorized or illegal withdrawals from the systems. Water audit improves the knowledge and documentation of the distribution system, and better understanding of what is happening to the water after it leaves the source point. Comprehensive water audit gives a detailed profile of the distribution system and water users, thereby facilitating easier and effective management of the resources with improved reliability. It helps in correct diagnosis of the problems faced in order to suggest optimum solutions. This leads to reduced water losses; improved financial performance; improved reliability of supply system; enhanced knowledge of the distribution; efficient use of existing supplies; better safeguard to public health and property; improved public relations; reduced legal liability and reduced disruption etc. thereby improving level of service to customers. It is thus an effective tool for realistic understanding and assessment of the present performance level and efficiency of the service and the adaptability of the system for future expansion & rectification of faults during modernization. 
    """
    summary_paragraph = Paragraph(summary_text, summary_style)
    elements.append(summary_paragraph)
    elements.append(Spacer(1, 24))
    
    title_paragraph = Paragraph("Steps Of WATER AUDIT", title_style)
    elements.append(title_paragraph)
    
    
    summary_text = f"""
    Water Audit includes water supply and usage study, process study, system audit, discharge analysis and preparation of water audit report.
    """
    summary_paragraph = Paragraph(summary_text, summary_style)
    elements.append(summary_paragraph)
    elements.append(Spacer(1, 24))
    
    title_paragraph = Paragraph("Water Supply and Usage Study ", title_style)
    elements.append(title_paragraph)
    
    
    summary_text = f"""
    Water audit comprises preparation of layout of water sources, distribution network, and service/delivery points to water users and return flow of waste or excess water. The layout should contain locations and flow measurement devices installed at key points in the water supply system.
    """
    summary_paragraph = Paragraph(summary_text, summary_style)
    elements.append(summary_paragraph)
    elements.append(Spacer(1, 24))
    
    title_paragraph = Paragraph("Process Study", title_style)
    elements.append(title_paragraph)
    
    
    summary_text = f"""
    Flow measurement devices were installed at all strategic points to calculate the water consumption at The Leela Palace, Udaipur in various activities such as supply to the Guest rooms, plantation, Kitchen, canteens, toilets etc. Water quality of the distribution system needs to be monitored regularly at strategic points to find out the level and nature of contaminants present in the supplied water. Study of water test reports conducted and its analyse as per the norms

    """
    summary_paragraph = Paragraph(summary_text, summary_style)
    elements.append(summary_paragraph)
    elements.append(PageBreak())
    
    title_paragraph = Paragraph("System Audit", title_style)
    elements.append(title_paragraph)
    
    
    summary_text = f"""
    The current water usages and systems for water use under various sectors needed to be studied to check their operational efficiency and level of maintenance. The scope for any modification or up- gradation will depend on the status of existing systems. Measurement methodology from the intake point of the system through various sub-systems to the ultimate user points needs to be verified periodically for its suitability, efficiency and accuracy. Bulk metering should be done at the source for zones, districts, etc. and revenue metering for consumers. This will help in identifying the reaches of undue water wastage. The domestic wastewater return flows from canteen, bathroom and effluents from the ETP needs to be studied for conformity to environment standards, possibility of recovery of valuable by-products and the opportunity for recycling of waste water (which is happening at present). 

    """
    summary_paragraph = Paragraph(summary_text, summary_style)
    elements.append(summary_paragraph)
    elements.append(Spacer(1, 24))
    
    title_paragraph = Paragraph("Water Audit Report ", title_style)
    elements.append(title_paragraph)
    
    
    summary_text = f"""
    A water audit can be accomplished on the basis of water allotted for a service and water actually utilized for that service. After assessing the loss of water and the efficiency of the system, steps needed for utilization of recoverable water loss and reuse may be listed. An effective water audit report may be purposeful in detection of water losses and improve efficiency of the system. Water audit of the system should be undertaken at regular intervals, at least on an annual basis. ITIFY water audit report explains the losses of water in system and various management approaches for The Leela Palace


    """
    summary_paragraph = Paragraph(summary_text, summary_style)
    elements.append(summary_paragraph)
    elements.append(Spacer(1, 24))
    elements.append(PageBreak())
    
    return elements

def create_introduction(styles, user):
    user_details = get_object_or_404(BasicDetails, user=user)
    elements = []

    # Title setup
    title_style = styles['Title'].clone('TitleStyle')
    title_style.fontSize = 22
    title_style.textColor = colors.navy
    title_style.alignment = TA_CENTER
    title_paragraph = Paragraph("<a name='intro'/> Introduction", title_style)
    elements.append(title_paragraph)
    elements.append(Spacer(1, 18))
    
    # Introduction content
    summary_style = styles['BodyText'].clone('SummaryStyle')
    summary_style.alignment = TA_JUSTIFY
    summary_style.fontSize = 12
    summary_style.spaceBefore = 6
    summary_style.spaceAfter = 6
    # add vertical space between lines
    summary_style.leading = 14
    summary_text = f"""
    The Digital Water Audit Report for <b>{user_details.organization_name}</b> summarizes the key findings, recommendations, and insights from the comprehensive water audit conducted at {user_details.address}. Key findings highlight areas of potential improvement, cost savings, and environmental benefits. Recommendations are intended to guide strategic decisions to enhance water efficiency and sustainability.
    """
    summary_paragraph = Paragraph(summary_text, summary_style)
    elements.append(summary_paragraph)
    elements.append(Spacer(1, 24))
    
    title_style = styles['Title'].clone('TitleStyle')
    title_style.fontSize = 18
    title_style.textColor = colors.olivedrab
    title_style.alignment = TA_LEFT
    title_paragraph = Paragraph("Fresh Water Sources", title_style)
    elements.append(title_paragraph)
    
    # sources of water
    sources = SourceWaterProfile.objects.filter(user=user)
    
    # show the sources of water, daily consumption and cost in a table
    table_data = [
        ['Source of Water', 'Daily Consumption (KL)', 'Cost (INR)'],
    ]
    for source in sources:
        table_data.append([source.source_name, source.source_daily_consumption, source.source_water_cost])
    # calculate total daily cost by multiplying daily consumption with cost
    total_cost = 0
    for source in sources:
        total_cost += source.source_daily_consumption * source.source_water_cost
        
    table_data.append(['Total Daily Consumption', '', total_cost])
    
    table = Table(table_data, colWidths=[133.33, 133.33, 133.33], spaceBefore=20, spaceAfter=20)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.darkblue),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),

    ])
    table.setStyle(table_style)
    elements.append(table)
    
    title_paragraph = Paragraph("Available Tanks", title_style)
    elements.append(title_paragraph)
    
    # tanks and capacities
    tanks = TanksCapacities.objects.filter(user=user)
    
    # show the tanks and capacities in a table
    table_data = [
        ['Tank Name', 'Capacity (KL)']
    ]
    for tank in tanks:
        table_data.append([tank.name, tank.capacity])
    # total capacity
    total_capacity = sum([tank.capacity for tank in tanks])
    table_data.append(['Total Capacity', f'{total_capacity} KL'])
    
    table = Table(table_data, colWidths=[200, 200], spaceBefore=20, spaceAfter=20)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.darkblue),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        
    ])
    table.setStyle(table_style)
    elements.append(table)
    
    
    
    
    elements.append(PageBreak())
    
    
    
    return elements


def generate_pdf_file(user_details):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    doc.onFirstPage = lambda canvas, doc: canvas.setTitle("Digital Water Audit Report")
    
    styles = initialize_styles()
    elements = []
    elements.extend(create_title_page(styles, user_details))
    elements.extend(create_index_page(styles))
    elements.extend(create_executive_summary(styles, user_details))
    elements.extend(create_introduction(styles, user_details))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


@login_required
def generate_pdf(request):
    
    # Generate PDF
    pdf_content = generate_pdf_file(request.user)
    
    response = FileResponse(pdf_content, filename='report.pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    return response
