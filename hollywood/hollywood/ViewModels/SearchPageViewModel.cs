using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Forms;

using hollywood.Models;

namespace hollywood.ViewModels
{
    class SearchPageViewModel : BaseViewModel
    {
        ObservableCollection<Item> _searchResults;
        readonly ICommand _searchCommand;

        public SearchPageViewModel() 
        {
            _searchCommand = new Command<string>(async (text) => await OnSearchTextChange(text));
        }

        public ObservableCollection<Item> SearchResults 
        {
            get { return _searchResults; }
            private set { SetProperty(ref _searchResults, value); }
        }

        public ICommand SearchCommand 
        {
            get { return _searchCommand; }
        }

        async Task OnSearchTextChange(string searchTerm) 
        {
            try
            {
                SearchResults = await App.ApiConnection.GetSearchResults(searchTerm);
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                throw ex; // TODO: Make a popup or something??
            }
        }
    }
}
