using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Text;
using hollywood.Models;

namespace hollywood.Services
{
    public interface IContextService : INotifyPropertyChanged
    {
        Context Context {
            get;
            set;
        }
        
    }
}
