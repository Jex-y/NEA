using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.CompilerServices;
using System.IO;
using Newtonsoft.Json;
using Xamarin.Forms;

using hollywood.Models;
using hollywood.Services;

using Context = hollywood.Models.Context;
using Debug = System.Diagnostics.Debug;
using System.ComponentModel;

[assembly: Xamarin.Forms.Dependency(typeof(hollywood.Droid.Services.ContextService))]
namespace hollywood.Droid.Services
{
    public class ContextService : IContextService
    {
        public ContextService() 
        {
            _context = GetContext().Result;
            PropertyChanged += async (sender, args) => await SaveContext();
            _context.Basket.OrderUpdated += async (sender, args) => await SaveContext();
        }

        string fileName = Path.Combine(System.Environment.GetFolderPath(System.Environment.SpecialFolder.Personal), "contextsdfghjkl.json");
        Context _context = null;

        public Context Context {
            get { return GetContext().Result; }
            set { SetProperty( ref _context, value); } 
        }

        async Task<Context> GetContext() 
        {
            if (_context is null)
            {
                if (!await LoadContext())
                {
                    _context = new Context
                    {
                        Basket = new Order()
                    };
                }
                else 
                {
                    if (_context.LastModified < DateTime.Now.AddHours(Constants.MaxAge))
                    {
                        _context = new Context
                        {
                            Basket = new Order()
                        };
                    }
                }
            }
            return _context;
        }

        async Task<bool> LoadContext() 
        {
            bool result = false;
            if (File.Exists(fileName)) 
            {
                // string content = await File.ReadAllTextAsync(fileName);
                // TODO: Investigate why this doesn't work 
                string content = File.ReadAllText(fileName);
                Debug.WriteLine(content);
                _context = JsonConvert.DeserializeObject<Context>(content);
                result = true;
            }
            
            return result;
        }

        async Task SaveContext() 
        {
            _context.LastModified = DateTime.Now;
            string content = JsonConvert.SerializeObject(_context);
            await File.WriteAllTextAsync(fileName, content);
            Debug.WriteLine(content);
        }

        protected bool SetProperty<T>(ref T backingStore, T value,
            [CallerMemberName] string propertyName = "",
            Action onChanged = null)
        {
            if (EqualityComparer<T>.Default.Equals(backingStore, value))
                return false;

            backingStore = value;
            onChanged?.Invoke();
            OnPropertyChanged(propertyName);
            return true;
        }

        #region INotifyPropertyChanged
        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string propertyName = "")
        {
            var changed = PropertyChanged;
            if (changed == null)
                return;

            changed.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
        #endregion
    }
}