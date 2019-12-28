# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from mongoengine import StringField, IntField, BooleanField, MultiLineStringField, URLField, DecimalField, Document

A = 'A'
B = 'B'
N = 'N'
AREAS = (
    (A, 'A'),
    (B, 'B'),
    (N, 'N')
)

TRUE = 'Y'
FALSE = 'N'
N_I = '-'
N_A = 'NA'
OPTIONS = (
    (TRUE, 'yes'),
    (FALSE, 'no'),
    (N_I, 'No information available'),
    (N_A, 'Not applied')
)

UNA = '1'
DOS = '2'
TRES = '3'
CUATRO = '4'
CINCO = '5'
STARS = (
    (UNA, '1'),
    (DOS, '2'),
    (TRES, '3'),
    (CUATRO, '4'),
    (CINCO, '5'),
    (N_I, 'No information available'),
    (N_A, 'Not applied')
)

CHAIN = 'chain'
INDEPENDENT = 'independent'
GROUP = 'group'
MANAGEMENT = (
    (CHAIN, 'Chain'),
    (INDEPENDENT, 'Independent'),
    (GROUP, 'group'),
    (N_I, 'No information available')
)

TYPOLOGY_HOTEL = 'hotel'
TYPOLOGY_APARTHOTEL = 'aparthotel'
TYPOLOGY_BUDGET = 'budget'
TYPOLOGY_HOSTEL = 'hostel'
TYPOLOGY_APARTMENT = 'apartment'
TYPOLOGY = (
    (TYPOLOGY_HOTEL, 'Hotel'),
    (TYPOLOGY_APARTHOTEL, 'Aparthotel'),
    (TYPOLOGY_BUDGET, 'Budget'),
    (TYPOLOGY_HOSTEL, 'Hostel'),
    (TYPOLOGY_APARTMENT, 'Apartment'),
    (N_I, 'No information available')
)

SEGMENT_BOUTIQUE = 'boutique'
SEGMENT_STANDARD = 'standard'
SEGMENT_APART_BOUTIQUE = 'apart_boutique'
SEGMENT_BUDGET = 'budget'
SEGMENT_APART_TOURISTIC = 'apart_touristic'
SEGMENT_LUXURY = 'luxury'
SEGMENT_HOSTEL = 'hostel'
SEGMENT_SMART_BOUTIQUE = 'smart_boutique'
SEGMENT_UPSCALE = 'upscale'
SEGMENT_BASIC_CHIC = 'basic_chic'
SEGMENT_CHIC_HOSTEL = 'chic_hostel'
SEGMENT_MODERN = 'modern'
SEGMENT = (
    (SEGMENT_BOUTIQUE, 'Boutique'),
    (SEGMENT_STANDARD, 'Standard'),
    (SEGMENT_BUDGET, 'Budget'),
    (SEGMENT_APART_BOUTIQUE, 'Apart-Boutique'),
    (SEGMENT_APART_TOURISTIC, 'Apart-Touristic'),
    (SEGMENT_LUXURY, 'Luxury'),
    (SEGMENT_HOSTEL, 'boutique'),
    (SEGMENT_SMART_BOUTIQUE, 'Smart-Boutique'),
    (SEGMENT_UPSCALE, 'Upscale'),
    (SEGMENT_BASIC_CHIC, 'Basic chic'),
    (SEGMENT_CHIC_HOSTEL, 'Chic hostel'),
    (SEGMENT_MODERN, 'Modern'),
    (N_I, 'No information available')
)


class Hotel(Document):
    id = IntField()
    name = StringField(max_length=200)
    test = BooleanField(default=True)
    target_area = StringField(required=False, max_length=1, choices=AREAS)
    selection = StringField(required=False, choices=OPTIONS)
    district = StringField(required=False)
    postal_code = StringField(required=False)
    address = MultiLineStringField(required=False)
    web = URLField(required=False)
    stars = StringField(choices=STARS)
    management = StringField(choices=MANAGEMENT, default=N_I)
    brand_name = StringField(default=N_I)
    typology = StringField(choices=TYPOLOGY, default=N_I)
    segment_style = StringField(choices=SEGMENT, default=N_I)
    m2_built = IntField(required=False)
    m2_built_per_hab = DecimalField(required=False)
    pax_beds = IntField(required=False)
    rooms = IntField(required=False)
    std = IntField(required=False)
    dis = IntField(required=False)
    sin = IntField(required=False)
    exe = IntField(required=False)
    js = IntField(required=False)
    sui = IntField(required=False)
    psui = IntField(required=False)
    ap = IntField(required=False)
    num_salas = IntField(required=False)
    m2_salas = IntField(required=False)
    salas_pax = IntField(required=False)
    business_center = StringField(required=False, choices=OPTIONS)
    restaurante = IntField(required=False)
    bar = IntField(required=False)
    fitness = StringField(required=False, choices=OPTIONS)
    belleza = StringField(required=False, choices=OPTIONS)
    sauna_turco = StringField(required=False, choices=OPTIONS)
    pool_interior = StringField(required=False, choices=OPTIONS)
    pool_exterior = StringField(required=False, choices=OPTIONS)
    terraza_azotea = StringField(required=False, choices=OPTIONS)
    parking = StringField(required=False, choices=OPTIONS)
    sellos_calidad_sostenibilidad = StringField(required=False)
    additional_services = StringField(required=False)
    points_bk = DecimalField(required=False)
    ta_rank = IntField(required=False)
    total_rank = IntField(required=False)
    points_ta = DecimalField(required=False)
    q_reviews = IntField(required=False)
    price_booking = IntField(required=False)
    price_min_ta = IntField(required=False)
    price_max_ta = IntField(required=False)
    price_bar_per_2 = IntField(required=False)
    price_band = IntField(required=False)
    notas = MultiLineStringField(required=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    description = models.TextField(default="")

    def __unicode__(self):  # 0 param method
        return self.name