from typing import Any

from apps.administration import forms
from apps.main.models import (
    Banner,
    CompanyInfo,
    ContactEmail,
    ContactPhone,
    SiteImage,
    SiteText,
    SocialMediaLink,
)
from apps.orders.models import Order
from apps.store.models import (
    Brand,
    Category,
    CategoryAttribute,
    Collection,
    Product,
    ProductImage,
    ProductInformation,
)
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core import paginator
from django.db import transaction
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "administration/index.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["creator_dashboards"] = [
            {
                "name": _("Banners"),
                "route": reverse("apps.administration:banner-list-create"),
            },
            {
                "name": _("Categories"),
                "route": reverse("apps.administration:store-category-list-create"),
                "permission": "store.view_category",
            },
            {
                "name": _("Brands"),
                "route": reverse("apps.administration:store-brand-list-create"),
                "permission": "store.view_brand",
            },
            {
                "name": _("Collection"),
                "route": reverse("apps.administration:store-collection-list-create"),
                "permission": "store.view_collection",
            },
            {
                "name": _("Products"),
                "route": reverse("apps.administration:store-product-list"),
                "permission": "store.view_product",
            },
            {
                "name": _("Orders"),
                "route": reverse("apps.administration:order-list"),
                "permission": "orders.view_order",
            },
            {
                "name": _("About Us"),
                "route": reverse("apps.administration:about"),
                "permission": "main.view_sitetext",
            },
            {
                "name": _("Privacy Policy"),
                "route": reverse("apps.administration:privacy-policy"),
                "permission": "main.view_sitetext",
            },
            {
                "name": _("Delivery Policy"),
                "route": reverse("apps.administration:delivery-policy"),
                "permission": "main.view_sitetext",
            },
            {
                "name": _("Contact"),
                "route": reverse("apps.administration:contact"),
                "permission": "main.view_companyinfo",
            },
            {
                "name": _("Site Images"),
                "route": reverse("apps.administration:site-images"),
                "permission": "main.view_siteimage",
            },
            {
                "name": _("Users"),
                "route": reverse("apps.administration:user-list"),
                "permission": "auth.view_user",
            },
        ]
        return context


class PrivacyPolicyView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "administration/privacy-policy.html"
    http_method_names = ["get", "post"]
    form_class = forms.PrivacyPolicyTextFormSet
    redirect_url_name = "apps.administration:privacy-policy"
    permission_required = ["main.view_sitetext", "main.add_sitetext", "main.change_sitetext"]

    def get(self, request):
        if SiteText.objects.count() == 0:
            SiteText.site_texts.create_many_by_languages(languages=settings.LANGUAGES)
        site_texts = SiteText.objects.all().order_by("language").only("language", "privacy_policy")
        form = self.form_class(initial=site_texts)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(
            initial=SiteText.objects.all().order_by("language").only("language", "privacy_policy"),
            data=request.POST,
        )
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Privacy Policy texts were saved successfully!"))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("Privacy Policy texts cannot be saved!"))
        messages.error(request, _("Privacy Policy texts cannot be saved!"))
        return render(request, self.template_name, {"form": form})


class DeliveryPolicyView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "administration/delivery-policy.html"
    http_method_names = ["get", "post"]
    form_class = forms.DeliveryPolicyTextFormSet
    redirect_url_name = "apps.administration:delivery-policy"
    permission_required = ["main.view_sitetext", "main.add_sitetext", "main.change_sitetext"]

    def get(self, request):
        if SiteText.objects.count() == 0:
            SiteText.site_texts.create_many_by_languages(languages=settings.LANGUAGES)
        site_texts = SiteText.objects.all().order_by("language").only("language", "delivery")
        form = self.form_class(initial=site_texts)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(
            initial=SiteText.objects.all().order_by("language").only("language", "delivery_policy"),
            data=request.POST,
        )
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Delivery Policy texts were saved successfully!"))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("Delivery Policy texts cannot be saved!"))
        messages.error(request, _("Delivery Policy texts cannot be saved!"))
        return render(request, self.template_name, {"form": form})


class AboutView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "administration/about.html"
    http_method_names = ["get", "post"]
    form_class = forms.AboutTextFormSet
    redirect_url_name = "apps.administration:about"
    permission_required = ["main.view_sitetext", "main.add_sitetext", "main.change_sitetext"]

    def get(self, request):
        if SiteText.objects.count() == 0:
            SiteText.site_texts.create_many_by_languages(languages=settings.LANGUAGES)
        site_texts = SiteText.objects.all().order_by("language").only("language", "about")
        form = self.form_class(initial=site_texts)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(
            initial=SiteText.objects.all().order_by("language").only("language", "about"),
            data=request.POST,
        )
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("About Us texts were saved successfully!"))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("About Us texts cannot be saved!"))
        messages.error(request, _("About Us texts cannot be saved!"))
        return render(request, self.template_name, {"form": form})


class ContactView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "administration/contact.html"
    http_method_names = ["get"]
    social_media_link_form_class = forms.SocialMediaLinkForm
    contact_phone_form_class = forms.ContactPhoneForm
    contact_email_form_class = forms.ContactEmailForm
    company_info_form_class = forms.CompanyInfoFormSet
    permission_required = [
        "main.view_companyinfo",
        "main.view_contactemail",
        "main.view_contactphone",
        "main.view_socialmedialink",
    ]

    def get(self, request):
        if CompanyInfo.objects.count() == 0:
            CompanyInfo.company_infos.create_many_by_languages(languages=settings.LANGUAGES)
        social_media_link_form = self.social_media_link_form_class()
        contact_email_form = self.contact_email_form_class()
        contact_phone_form = self.contact_phone_form_class()
        company_info_form = self.company_info_form_class(initial=CompanyInfo.objects.all())
        social_media_links = SocialMediaLink.objects.all()
        contact_emails = ContactEmail.objects.all()
        contact_phones = ContactPhone.objects.all()
        return render(
            request,
            self.template_name,
            {
                "social_media_link_form": social_media_link_form,
                "contact_email_form": contact_email_form,
                "company_info_form": company_info_form,
                "contact_phone_form": contact_phone_form,
                "social_media_links": social_media_links,
                "contact_emails": contact_emails,
                "contact_phones": contact_phones,
            },
        )


class ContactEmailCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ContactEmail
    form_class = forms.ContactEmailForm
    http_method_names = ["post"]
    success_message = _("Contact email was added successfully!")
    permission_required = ["main.add_contactemail"]

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#contact-email-form"


class ContactEmailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ContactEmail
    success_message = _("Contact email was deleted successfully!")
    permission_required = ["main.delete_contactemail"]

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#contact-email-form"


class ContactPhoneCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ContactPhone
    form_class = forms.ContactPhoneForm
    http_method_names = ["post"]
    success_message = _("Contact phone was added successfully!")
    permission_required = ["main.add_contactphone"]

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#contact-phone-form"


class ContactPhoneDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ContactPhone
    success_message = _("Contact phone was deleted successfully!")
    permission_required = ["main.delete_contactphone"]

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#contact-phone-form"


class SocialMediaLinkCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = SocialMediaLink
    form_class = forms.SocialMediaLinkForm
    http_method_names = ["post"]
    success_message = _("Social media link was added successfully!")
    permission_required = ["main.add_socialmedialink", "main.view_socialmedialink"]

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#social-media-link-form"


class SocialMediaLinkDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SocialMediaLink
    success_message = _("Social media link was deleted successfully!")
    permission_required = ["main.delete_socialmedialink"]

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#social-media-link-form"


class CompanyInfoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, TemplateView):
    model = CompanyInfo
    form_class = forms.CompanyInfoFormSet
    http_method_names = ["post"]
    success_message = _("Company info was saved successfully!")
    redirect_url_name = "apps.administration:contact"
    permission_required = ["main.add_companyinfo", "main.view_companyinfo"]

    def post(self, request):
        form = self.form_class(initial=CompanyInfo.company_infos.list_queryset(), data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Company info was saved successfully!"))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("Company info cannot be saved!"))
        messages.error(request, _("Company info cannot be saved!"))
        return redirect(self.redirect_url_name)

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#company-info-form"


class SiteImagesView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = SiteImage
    template_name = "administration/site-images.html"
    http_method_names = ["get", "post"]
    form_class = forms.SiteImageForm
    redirect_url_name = "apps.administration:site-images"
    permission_required = ["main.add_siteimage", "main.view_siteimage"]

    def get(self, request):
        try:
            site_image = self.model.objects.first()
        except self.model.DoesNotExist:
            site_image = self.model.objects.create()
        form = self.form_class(instance=site_image)
        return render(request, self.template_name, {"form": form, "site_image": site_image})

    def post(self, request):
        form = self.form_class(instance=self.model.objects.first(), data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Site images were saved successfully!"))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("Site images cannot be saved!"))
        messages.error(request, _("Site images cannot be saved!"))
        return render(request, self.template_name, {"form": form})


class BannerListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Banner
    form_class = forms.BannerForm
    template_name = "administration/banners/index.html"
    success_message = _("Banner was created successfully!")
    success_url = reverse_lazy("apps.administration:banner-list-create")
    permission_required = ["main.add_banner", "main.view_banner"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banners"] = self.model.objects.all()
        return context


class BannerUpdateDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.BannerForm
    model = Banner
    template_name = "administration/banners/edit.html"
    context_object_name = "banner"
    permission_required = ["main.change_banner", "main.delete_banner"]

    def post(self, request, pk):
        banner = self.model.objects.get(pk=pk)
        form = self.form_class(instance=banner, data=request.POST, files=request.FILES)
        if self.request.POST.get("_method", None) == "delete":
            banner.delete()
            messages.success(request, _("Banner was deleted successfully"))
            return redirect(reverse("apps.administration:banner-list-create"))
        if form.is_valid():
            form.save()
            messages.success(request, _("Banner was updated successfully"))
            return redirect(reverse("apps.administration:banner-update-delete", kwargs={"pk": banner.pk}))
        return render(request, self.template_name, {"form": form, "banner": banner})


# AUTH
class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy("apps.main:index")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "administration/auth/profile.html"
    http_method_names = ["get", "post"]
    form_class = forms.UserUpdateForm
    redirect_url_name = "apps.administration:auth-profile"

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(instance=request.user, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("User information were saved successfully!"))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("User information cannot be saved!"))
        messages.error(request, _("User information cannot be saved!"))
        return render(request, self.template_name, {"form": form})


class LoginView(auth_views.LoginView):
    authentication_form = forms.LoginForm
    redirect_field_name = reverse_lazy("apps.administration:index")
    redirect_authenticated_user = True
    template_name = "administration/auth/login.html"


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = "administration/auth/password-change.html"
    success_url = reverse_lazy("apps.administration:auth-profile")
    form_class = forms.PasswordChangeForm


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = "administration/users/list.html"
    context_object_name = "users"
    permission_required = ["auth.view_user"]

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_superuser=False, is_staff=False)


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = forms.UserCreateForm
    login_url = reverse_lazy("apps.administration:index")
    template_name = "administration/users/create.html"
    success_message = _("User was created successfully!")
    success_url = reverse_lazy("apps.administration:user-list")
    permission_required = ["auth.add_user"]

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_superuser=False, is_staff=False)


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    success_message = _("User was deleted successfully!")
    success_url = reverse_lazy("apps.administration:user-list")
    permission_required = ["auth.delete_user"]

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_superuser=False, is_staff=False)


# STORE
class CategoryListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = forms.CategoryForm
    template_name = "administration/store/categories/index.html"
    success_message = _("Category was created successfully!")
    success_url = reverse_lazy("apps.administration:store-category-list-create")
    permission_required = ["store.add_category", "store.view_category"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.model.categories.list_queryset()
        return context


class CategoryUpdateDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.CategoryForm
    attribute_form_class = forms.CategoryAttributeFormSet
    model = Category
    template_name = "administration/store/categories/edit.html"
    context_object_name = "category"
    permission_required = ["store.change_category", "store.delete_category"]

    def get_queryset(self):
        return super().get_queryset().prefetch_related("category_attribute")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if not hasattr(self.get_object(), "category_attribute") or len(
            self.get_object().category_attribute.all()
        ) < len(settings.LANGUAGES):
            CategoryAttribute.objects.bulk_create(
                [
                    CategoryAttribute(language=lang[0], category=self.get_object())
                    for lang in settings.LANGUAGES
                ]
            )
        context["attribute_form"] = self.attribute_form_class(instance=self.get_object())
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        category = self.get_object()
        form = self.form_class(data=request.POST, instance=category, files=request.FILES)
        attribute_form = self.attribute_form_class(
            data=self.request.POST,
            instance=category,
        )
        try:
            if self.request.POST.get("_method", None) == "delete":
                category.delete()
                messages.success(request, _("Category was deleted successfully"))
                return redirect(reverse("apps.administration:store-category-list-create"))
            if form.is_valid() and attribute_form.is_valid():
                category = form.save()
                attribute_form.save()
                messages.success(request, _("Category was updated successfully"))
                return redirect(
                    reverse(
                        "apps.administration:store-category-update-delete",
                        kwargs={"pk": category.pk},
                    )
                )
        except ProtectedError:
            messages.error(request, _("Category is dependent on another category"))
            return redirect(
                reverse(
                    "apps.administration:store-category-update-delete",
                    kwargs={"pk": category.pk},
                )
            )
        return render(
            request,
            self.template_name,
            {"form": form, "category": category, "attribute_form": attribute_form},
        )


class BrandListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Brand
    form_class = forms.BrandForm
    template_name = "administration/store/brands/index.html"
    success_message = _("Brand was created successfully!")
    success_url = reverse_lazy("apps.administration:store-brand-list-create")
    permission_required = ["store.add_brand", "store.view_brand"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brands"] = self.model.objects.all()
        return context


class BrandUpdateDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.BrandForm
    model = Brand
    template_name = "administration/store/brands/edit.html"
    context_object_name = "brand"
    permission_required = ["store.change_brand", "store.delete_brand"]

    def post(self, request, pk):
        brand = self.model.objects.get(pk=pk)
        form = self.form_class(instance=brand, data=request.POST, files=request.FILES)
        if self.request.POST.get("_method", None) == "delete":
            brand.delete()
            messages.success(request, _("Brand was deleted successfully"))
            return redirect(reverse("apps.administration:store-brand-list-create"))
        if form.is_valid():
            form.save()
            messages.success(request, _("Brand was updated successfully"))
            return redirect(
                reverse(
                    "apps.administration:store-brand-update-delete",
                    kwargs={"pk": brand.pk},
                )
            )
        return render(request, self.template_name, {"form": form, "brand": brand})


class CollectionListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Collection
    form_class = forms.CollectionForm
    template_name = "administration/store/collections/index.html"
    success_message = _("Model was created successfully!")
    success_url = reverse_lazy("apps.administration:store-collection-list-create")
    permission_required = ["store.add_collection", "store.view_collection"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collections"] = self.model.objects.all()
        return context


class CollectionUpdateDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    form_class = forms.CollectionForm
    model = Collection
    template_name = "administration/store/collections/edit.html"
    context_object_name = "collection"
    permission_required = ["store.change_collection", "store.delete_collection"]

    def post(self, request, pk):
        collection = self.model.objects.get(pk=pk)
        form = self.form_class(instance=collection, data=request.POST, files=request.FILES)
        if self.request.POST.get("_method", None) == "delete":
            collection.delete()
            messages.success(request, _("Model was deleted successfully"))
            return redirect(reverse("apps.administration:store-collection-list-create"))
        if form.is_valid():
            form.save()
            messages.success(request, _("Model was updated successfully"))
            return redirect(
                reverse(
                    "apps.administration:store-collection-update-delete",
                    kwargs={"pk": collection.pk},
                )
            )
        return render(request, self.template_name, {"form": form, "collection": collection})


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = "administration/store/products/list.html"
    context_object_name = "products"
    permission_required = ["store.view_product"]

    def get_queryset(self):
        return self.model.admin_products.list_queryset().all()


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = forms.ProductForm
    product_information_form_class = forms.ProductInformationFormSet
    product_image_form_class = forms.ProductImageFormSet
    template_name = "administration/store/products/create.html"
    success_message = _("Product was created successfully")
    success_url = reverse_lazy("apps.administration:store-product-list")
    permission_required = ["store.add_product"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["product_information_formset"] = self.product_information_form_class(
            queryset=ProductInformation.objects.none()
        )
        context["product_image_formset"] = self.product_image_form_class(queryset=ProductImage.objects.none())
        return context

    @transaction.atomic
    def post(self, request):
        form = self.form_class(data=request.POST, files=request.FILES)
        product_image_formset = self.product_image_form_class(queryset=ProductImage.objects.none())
        product_information_formset = self.product_information_form_class(
            queryset=ProductInformation.objects.none()
        )
        if form.is_valid():
            product = form.save()
            product_image_formset = self.product_image_form_class(
                instance=product, data=self.request.POST, files=self.request.FILES
            )
            product_information_formset = self.product_information_form_class(
                instance=product, data=self.request.POST, files=self.request.FILES
            )
            if product_image_formset.is_valid() and product_information_formset.is_valid():
                product_image_formset.save()
                product_information_formset.save()
                messages.success(request, self.success_message)
                return redirect(self.success_url)
        messages.error(request, _("Product cannot be created"))
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product_image_formset": product_image_formset,
                "product_information_formset": product_information_formset,
            },
        )


class ProductUpdateDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = forms.ProductForm
    product_information_form_class = forms.ProductInformationFormSet
    product_image_form_class = forms.ProductImageFormSet
    template_name = "administration/store/products/edit.html"
    permission_required = ["store.change_product"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["product_information_formset"] = self.product_information_form_class(
            instance=self.get_object()
        )
        context["product_image_formset"] = self.product_image_form_class(instance=self.get_object())
        return context

    @transaction.atomic
    def post(self, request, pk):
        product = self.model.objects.get(pk=pk)
        form = self.form_class(instance=product, data=request.POST, files=request.FILES)
        product_image_formset = self.product_image_form_class(
            instance=product, data=self.request.POST, files=request.FILES
        )
        product_information_formset = self.product_information_form_class(
            instance=product, data=self.request.POST, files=request.FILES
        )
        if self.request.POST.get("_method", None) == "delete":
            product.delete()
            messages.success(request, _("Product was deleted successfully"))
            return redirect(reverse("apps.administration:store-product-list"))
        if form.is_valid() and product_image_formset.is_valid() and product_information_formset.is_valid():
            form.save()
            product_image_formset.save()
            product_information_formset.save()
            messages.success(request, _("Product was updated successfully"))
            return redirect(
                reverse(
                    "apps.administration:store-product-update-delete",
                    kwargs={"pk": product.pk},
                )
            )
        messages.error(request, _("Product cannot be updated"))
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": product,
                "product_image_formset": product_image_formset,
                "product_information_formset": product_information_formset,
            },
        )


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = "administration/orders/list.html"
    context_object_name = "orders"
    per_page = 10
    permission_required = ["orders.view_order"]

    def get_queryset(self):
        query_params = self.request.GET.copy()
        queryset = self.model.orders.list_queryset().all()
        if query_params.get("search"):
            queryset = queryset.filter(
                Q(name__icontains=query_params.get("search"))
                | Q(phone__icontains=query_params.get("search"))
                | Q(total_paid__icontains=query_params.get("search"))
                | Q(code__icontains=query_params.get("search"))
            )

        queryset = paginator.Paginator(
            queryset,
            query_params.get("paginate_by", self.per_page),
        ).get_page(query_params.get("page", 1))
        return queryset


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    template_name = "administration/orders/detail.html"
    context_object_name = "order"
    queryset = model.orders.detail_queryset()
    permission_required = ["orders.view_order"]
    status_form_class = forms.OrderStatusForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.get_object().mark_as_seen()
        context["status_form"] = self.status_form_class(instance=self.get_object())
        return context


class OrderStatusChangeView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    form_class = forms.OrderStatusForm
    permission_required = ["orders.change_order"]
    http_method_names = ["post"]
    success_message = _("Order status was updated successfully")

    def post(self, request, pk):
        order = self.model.objects.get(pk=pk)
        form = self.form_class(data=request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect("apps.administration:order-detail", pk=pk)
        messages.error(request, _("Order status cannot be updated"))
        return redirect("apps.administration:order-detail", pk=pk)
