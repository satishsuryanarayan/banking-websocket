from banking.apps.bank.v1.dtos.views.customersviewdto import CustomersViewDTO


class GetCustomerDTO(CustomersViewDTO):
    customer_id: int
