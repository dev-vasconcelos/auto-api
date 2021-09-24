using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;

namespace ${projectName}.Service.Interface {
    public interface IService<T> where T : ${projectName}.Models.AbstractEntity {
        T Save(T entity);
        T Update(T entity);
        bool Delete(T entity);
        bool Delete(long? id);
        List<T> Get();
        List<T> Get(Expression<Func<T, bool>> predicate, params string[] navProperties);
        T Get(T entity);
        T Get(long? id);
    }
}