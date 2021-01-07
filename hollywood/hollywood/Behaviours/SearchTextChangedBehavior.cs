using System;
using System.Collections.Generic;
using System.Text;
using Xamarin.Forms;

namespace hollywood.Behaviours
{
    class SearchTextChangedBehavior : Behavior<SearchBar>
    {
        protected override void OnAttachedTo(SearchBar bindable)
        {
            base.OnAttachedTo(bindable);
            bindable.TextChanged += Bindable_TextChanged;
        }

        protected override void OnDetachingFrom(SearchBar bindable)
        {
            base.OnDetachingFrom(bindable);
            bindable.TextChanged -= Bindable_TextChanged;
        }

        private void Bindable_TextChanged(object sender, TextChangedEventArgs args) 
        {
            ((SearchBar)sender).SearchCommand?.Execute(args.NewTextValue);
        }
    }
}
