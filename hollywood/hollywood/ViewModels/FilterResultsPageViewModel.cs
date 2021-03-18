using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using hollywood.Models;

namespace hollywood.ViewModels
{
    public class FilterResultsPageViewModel : BaseViewModel
    {
        ObservableCollection<Item> _items;

        public FilterResultsPageViewModel(ObservableCollection<Item> Items) 
        {
            this.Items = Items;
        }

        public ObservableCollection<Item> Items 
        {
            get { return _items; }
            set { SetProperty(ref _items, value); }
        }
    }
}
