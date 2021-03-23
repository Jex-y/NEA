using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using hollywood.Services;
using hollywood.Models;
using Xamarin.Forms;
using System.Diagnostics;
using hollywood.Views;

namespace hollywood.ViewModels
{
    class FilterPopupPageViewModel : BaseViewModel
    {
        readonly IRestService restService;
        ObservableCollection<Tag> _allTags;

        readonly ICommand _filterCommand;

        // If popup closed without add to basket, go back to initial order. 
        public FilterPopupPageViewModel()
        {
            restService = DependencyService.Get<IRestService>();
            _filterCommand = new Command(async () => await OnFilter());
            LoadTags();
        }

        async Task LoadTags() 
        {
            AllTags = await restService.GetAvailableTags();
        }

        async Task OnFilter()
        {
            ObservableCollection<Tag> selected = new ObservableCollection<Tag>();
            foreach (Tag tag in AllTags )
            {
                if (tag.FilterBy) 
                {
                    selected.Add(tag);
                }
            }

            ObservableCollection<Item> items = await restService.GetFilterResults(selected);

            App.Current.MainPage.Navigation.PushAsync(new FilterResultsPage(items));
        }

        public async Task OnToggle(object param) 
        {
            Debug.WriteLine(param);
        }

        public ObservableCollection<Tag> AllTags
        {
            get { return _allTags; }
            set { SetProperty(ref _allTags, value); }
        }
    }
}