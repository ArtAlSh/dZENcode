from django_filters import rest_framework as filters


class MessageFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="user__username", lookup_expr="startswith")
    email = filters.CharFilter(field_name="user__email", lookup_expr="startswith")
    order = filters.CharFilter(method="order_filter", help_text="desc or asc")

    def order_filter(self, queryset, name, value):
        order = "date" if value == "asc" else "-date"
        return queryset.order_by(order)
