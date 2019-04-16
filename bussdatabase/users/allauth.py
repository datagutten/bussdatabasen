class AccountAdapter(DefaultAccountAdapter):

  def get_login_redirect_url(self, request):
      return 'https://www.bussdatabasen.no/bevarte-busser/?page=%2Faccounts%2Fprofile'
