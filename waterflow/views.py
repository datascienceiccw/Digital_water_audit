from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import (
    SourceWaterProfile,
    RainWaterProfile,
    FreshWaterTreatmentProfile,
    BasicDetails,
    FreshWaterTreatmentProfileDetails,
    SourceWaterFlow,
    TanksCapacities,
    DrinkingWaterSource,
    RestaurantConsumption,
    KitchenDishwasherTapConsumption,
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
def basic_details(request):  # sourcery skip: assign-if-exp, merge-else-if-into-elif
    current_user = request.user
    details = BasicDetails.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = BasicDetailsForm(request.POST or None, initial={'organization_type':'Hospitality'})
        if form.is_valid():
            form.instance.user = current_user
            form.save()
            return redirect("source-water-profile/")
        else:
            print(form.errors)
    else:
        if details:
            form = BasicDetailsForm(instance=details)
        else:
            form = BasicDetailsForm()
    return render(request, "BasicDetails.html", {"form": form, "details": details})


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
            source_name = form.cleaned_data["source_name"]
            if SourceWaterProfile.objects.filter(
                user=current_user, source_name=source_name
            ).exists():
                form.add_error("source_name", "Source Water Profile already exists")
            else:
                form.instance.user = current_user
                form.save()
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
    print(is_rainwater_present)
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
    if request.method == "POST":
        form = FreshWaterTreatmentProfileForm(request.POST)
        if form.is_valid():
            current_user = request.user
            form.instance.user = current_user
            form.save()
            return redirect("fresh_water_treatment_profile")
        else:
            print(form.errors)
    else:
        form = FreshWaterTreatmentProfileForm()

    all_treatment_methods = FreshWaterTreatmentProfile.objects.filter(user=request.user)
    for method in all_treatment_methods:
        treatment_methods.append(method.name)
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
            print(profile_id_to_reset)
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


# previous implementation of flowchart_view using mermaid.js
# @login_required
# def flowchart_view(request):  # sourcery skip: dict-comprehension
#     current_user = request.user
#     source_water_profile = SourceWaterProfile.objects.filter(
#         user=current_user).all()
#     treatment_profile = FreshWaterTreatmentProfile.objects.filter(
#         user=current_user).all()
#     treatment_profile_seq_dic = {}
#     for treatment in treatment_profile:
#         treatment_profile_seq_dic[treatment.sequence_number] = treatment.name
#     mermaid_code = generate_mermaid_code(
#         current_user, source_water_profile, treatment_profile_seq_dic)

#     return render(request, 'flowchart.html', {'mermaid_code': mermaid_code})

# def source_water_mermaid_content(source_water_profile):
#     source_water_mermaid = """
#     style subgraphcontent fill:black,stroke:#333
#     subgraph subgraphcontent[<b> </b>]"""

#     # A dictionary to map source names for the Mermaid diagram
#     source_names = {
#         '1': 'Borewell Water',
#         '2': 'Tanker Water',
#         '3': 'Metro Water',
#         '4': 'Rain Water',
#         '5': 'Others'
#     }

#     # Iterate over each source water profile entry
#     for source in source_water_profile:
#         source_name = source_names.get(source.source_name, "Unknown")
#         source_consumption = source.source_daily_consumption
#         if source_consumption > 0:
#             source_water_mermaid += f'\n    style {source.source_name} fill:#1ca3ec,stroke:black,stroke-width:2px;'
#             source_water_mermaid += f'\n    {source.source_name}[({source_name})] -->|{source_consumption} kl| A[Total Source Water]'

#     source_water_mermaid += '''\nend \n'''
#     return source_water_mermaid


# def get_total_source_water(current_user):
#     source_water_profiles = SourceWaterProfile.objects.filter(user=current_user)
#     total_input_water = sum(profile.source_daily_consumption for profile in source_water_profiles)
#     return total_input_water


# def get_input_reject_water_from_treatments(current_user):
#     treatment_profiles = FreshWaterTreatmentProfile.objects.filter(
#         user=current_user).all()
#     dic = {}
#     for treatment in treatment_profiles:
#         dic[treatment.name] = (float(treatment.details.input_water), float(
#             treatment.details.reject_water))
#     return dic


# def fresh_water_treatment_mermaid_content(current_user, seq_dict):
#     total_source_water = get_total_source_water(current_user)
#     input_reject_dic = get_input_reject_water_from_treatments(current_user)
#     fresh_water_treatment_mermaid = """
#     style subgraphcontent1 fill:black,stroke:#333
#     subgraph subgraphcontent1[<b> </b>]\n
#     """
#     prev_node = 'A'
#     fresh_water_treatment_mermaid += f'   style {prev_node} fill:green,stroke:black,stroke-width:2px;\n'
#     fresh_water_treatment_mermaid += f'   {prev_node} --> |{total_source_water} kl| '

#     for key, value in sorted(seq_dict.items()):
#         main_node = chr(66 + key - 1)  # ASCII character starting from 'B'
#         # Additional node connected to each main node
#         aux_node = f'A{main_node}'

#         # Add main node and connect it to the auxiliary node
#         fresh_water_treatment_mermaid += f'{main_node}("{value}") -->|{input_reject_dic[value][1]} kl| {aux_node}("Reject")\n'
#         fresh_water_treatment_mermaid += f'style {aux_node} fill:red,stroke:black,stroke-width:2px;'
#         # Connect to the next main node if not the last key
#         if key != max(seq_dict.keys()):
#             next_main_node = chr(66 + key)
#             fresh_water_treatment_mermaid += f'   {main_node} --> |{input_reject_dic[value][0]} kl| {next_main_node}\n'
#             print(next_main_node)
#         else:
#           fresh_water_treatment_mermaid += f' {main_node} --> |{input_reject_dic[value][0]} kl| K[Tanks]\n'
#           fresh_water_treatment_mermaid += f'style K fill:green,stroke:black,stroke-width:2px;'


#     fresh_water_treatment_mermaid += '\nend'
#     return fresh_water_treatment_mermaid

# def generate_mermaid_code(current_user, source_water_profile, treatment_profile_seq_dic):
#     mermaid_code = """
#     graph TB;
#     style A fill:gray,stroke:black,stroke-width:2px;
#     """

#     mermaid_code += source_water_mermaid_content(source_water_profile)
#     mermaid_code += fresh_water_treatment_mermaid_content(
#         current_user, treatment_profile_seq_dic)
#     # print(mermaid_code)
#     return mermaid_code


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


@login_required
def flowchart_view(request):
    user = request.user
    sources_json = get_source_water(user)
    treatements_json = get_freshwater_treatment(user)

    context = {
        "sources": sources_json,
        "treatments": treatements_json,
    }
    return render(request, "flowchart.html", context)


@login_required
def tanks_capacities(request):
    if request.method == "POST":
        form = TanksCapacitiesForm(request.POST)
        if form.is_valid():
            current_user = request.user
            form.instance.user = current_user
            form.save()
            return redirect("tanks_capacities")
        else:
            print(form.errors)
    else:
        form = TanksCapacitiesForm()

    all_tanks = TanksCapacities.objects.filter(user=request.user)
    return render(
        request, "TanksCapacities.html", {"form": form, "all_tanks": all_tanks}
    )


@login_required
def delete_tanks_capacities(request):
    current_user = request.user
    TanksCapacities.objects.filter(user=current_user).delete()
    return redirect("tanks_capacities")


@login_required
def source_water_flow(request):
    current_user = request.user
    tank_names = [('1','Input freshwater tank'),
                ('2','Fire tank'),
                ('3','Softener Storage tank'),
                ('4','RO Storage tank'),
                ('5','Flush tank'),
                ('7','Domestic Water tank'),
                ('8','RO Input tank'),
                ('9','Boiler Makeup tank'),
                ('10','Others')]
    SOURCE_CHOICES = [
        ('1', 'Borewell Water'),
        ('2', 'Tanker water'),
        ('3', 'Metro/corporation Water'),
        ('4', 'Rainwater'),
        ('5', 'Others'),
    ]
    sources = []
    destinations = []
    fresh_water_sources = SourceWaterProfile.objects.filter(user=current_user)
    treatment_method = FreshWaterTreatmentProfile.objects.filter(user=current_user)
    tanks = TanksCapacities.objects.filter(user=current_user)
    for fresh_water_source in fresh_water_sources:
        sources.append(dict(SOURCE_CHOICES)[fresh_water_source.source_name])
    for method in treatment_method:
        sources.append(method.name)
        destinations.append(method.name)
    for tank in tanks:
        if tank=='10':
            sources.append(tank.other_tank_name)
            destinations.append(tank.other_tank_name)
        sources.append(dict(tank_names)[tank.name])
        destinations.append(dict(tank_names)[tank.name])

    template_sources = sources
    template_destinations = destinations
    form_sources = []
    form_destinations = []
    for source in range(len(sources)):
        form_sources.append((source,sources[source]))
    for destination in range(len(destinations)):
        form_destinations.append((destination,destinations[destination]))
    print(f'The destinations are {destinations}')
    print(f'The sources are {sources}')
    if request.method == "POST":
        form = SourceWaterFlowForm(request.POST,user=current_user)
        if form.is_valid():
            current_user = request.user
            form.instance.user = current_user
            form.save()
            return redirect('source-destination')
        else:
            print(form.errors)
    else:
        form = SourceWaterFlowForm(sources=form_sources,destinations=form_destinations)
    return render(request, "SourceWaterFlow.html", {'form': form, 'sources': sources, 'destinations': destinations})


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
            drinking_water_source = form.save(commit=False)
            drinking_water_source.user = current_user
            drinking_water_source.save()
            messages.success(request, "Drinking water source data saved successfully!")
            return redirect("kitchen_consumption")
    else:
        if details:
            form = DrinkingWaterSourceForm(instance=details)
        else:
            form = DrinkingWaterSourceForm()
    return render(
        request, "DrinkingWaterSource.html", {"form": form, "details": details}
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
            messages.success(request, "Banquet consumption data saved successfully!")
            return redirect("banquet_consumption")
    else:
        form = BanquetConsumptionForm()
    return render(
        request,
        "BanquetConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
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
            messages.success(request, "Guest Room consumption data saved successfully!")
            return redirect("guestroom_consumption")
    else:
        form = GuestRoomConsumptionForm()
    return render(
        request,
        "GuestRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
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
            return redirect("employeeroom_consumption")
    else:
        form = EmployeeRoomConsumptionForm()
    return render(
        request,
        "EmployeeRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
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
            return redirect("driversroom_consumption")
    else:
        form = DriversRoomConsumptionForm()
    return render(
        request,
        "DriversRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
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
    current_user = request.user
    details = SwimmingPoolConsumption.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = SwimmingPoolConsumptionForm(request.POST)
        if form.is_valid():
            swimmingpool_consumption = form.save(commit=False)
            swimmingpool_consumption.user = current_user
            swimmingpool_consumption.save()
            return redirect("waterbodies_consumption")
        else:
            print(form.errors)
    else:
        if details:
            form = SwimmingPoolConsumptionForm(instance=details)
        else:
            form = SwimmingPoolConsumptionForm()
    return render(
        request, "SwimmingPoolConsumption.html", {"form": form, "details": details}
    )


@login_required
def delete_swimmingpool_consumption(request):
    current_user = request.user
    SwimmingPoolConsumption.objects.filter(user=current_user).delete()
    return redirect("swimmingpool_consumption")


@login_required
def waterbodies_consumption_view(request):
    current_user = request.user
    details = WaterBodiesConsumption.objects.filter(user=current_user).first()
    print(details)
    if request.method == "POST":
        print('post')
        form = WaterBodiesConsumptionForm(request.POST)
        if form.is_valid():
            print('form')
            waterbody_consumption = form.save(commit=False)
            waterbody_consumption.user = current_user
            waterbody_consumption.save()
            return redirect("laundry_consumption")
        else:
            print(form.errors)
    else:
        if details:
            form = WaterBodiesConsumptionForm(instance=details)
        else:
            form = WaterBodiesConsumptionForm()
    return render(
        request, "WaterBodiesConsumption.html", {"form": form, "details": details}
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
            return redirect("boiler_consumption")
    else:
        if details:
            form = LaundryConsumptionForm(instance=details)
        else:
            form = LaundryConsumptionForm()
    return render(
        request, "LaundryConsumption.html", {"form": form, "details": details}
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

    return render(
        request,
        "BoilerConsumption.html",
        {
            "consumption_form": consumption_form,
            "details": consumption_details,
            "all_details": all_details,
            "all_treatment_methods": all_treatment_methods,
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
            return redirect("calorifier_consumption")
    else:
        form = CalorifierConsumptionForm()
    return render(
        request,
        "CalorifierConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
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
            return redirect("add_coolingtower")
    else:
        form = AddCoolingTowerConsumptionForm()
    return render(
        request,
        "AddCoolingTowerConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
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
            return redirect("other_consumption")
    else:
        if details:
            form = IrrigationConsumptionForm(instance=details)
        else:
            form = IrrigationConsumptionForm()

    return render(
        request,
        "IrrigationConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
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
            return redirect("wastewater_treatment")
    else:
        if details:
            form = OtherConsumptionForm(instance=details)
        else:
            form = OtherConsumptionForm()

    return render(
        request,
        "OtherConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
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
    print(water_treatment_details)

    if request.method == "POST":
        form = TanksAndCapacitiesForm(request.POST)

        if form.is_valid():
            tanks_and_capacities = form.save(commit=False)
            tanks_and_capacities.user = current_user
            tanks_and_capacities.save()
            return redirect("water_quality_profile")
    else:
        if details:
            form = TanksAndCapacitiesForm(instance=details)
        else:
            form = TanksAndCapacitiesForm()

    return render(
        request,
        "TanksAndCapacities.html",
        {
            "form": form,
            "details": details,
            "water_treatment_details": water_treatment_details,
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