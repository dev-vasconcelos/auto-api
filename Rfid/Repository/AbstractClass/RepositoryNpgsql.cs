using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Rfid.DataBase;
using Rfid.Models;
using Rfid.Repository.Interface;

namespace Rfid.Repository.AbstractClass
{
    public class RepositoryNpgsql<T> : IRepository<T> where T : AbstractEntity
    {
        protected NpgContext _context;

        public RepositoryNpgsql(NpgContext context)
        {
            _context = context;
        }

        public virtual T Save(T entity)
        {
            try
            {

                _context.Add(entity);
                _context.SaveChanges();
            }
            catch (System.Exception ex)
            {
                throw new Exception("Falha ao tentar salvar a entidade", ex);
            }

            return entity;
        }

        public virtual T Update(T entity)
        {
            try
            {
                _context.Attach<T>(entity).State = Microsoft.EntityFrameworkCore.EntityState.Modified;
                _context.Entry<T>(entity).Property(x => x.ScopeId).IsModified = false;
                _context.SaveChanges();

            }
            catch (System.Exception ex)
            {
                throw new Exception("Falha ao tentar atualizar entidade", ex);
            }
            return entity;
        }
        public virtual bool Delete(T entity)
        {
            try
            {
                _context.Remove(entity);
                _context.SaveChanges();
            }
            catch (System.Exception ex)
            {
                throw new Exception("Falha ao tentar apagar entidade", ex);
            }

            return true;
        }

        public virtual bool Delete(long? id)
        {
            try
            {
                _context.Remove(id);
                _context.SaveChanges();
            }
            catch (System.Exception ex)
            {
                throw new Exception("Falha ao tentar apagar entidade", ex);
            }

            return true;
        }

        public virtual List<T> Get() => _context.Set<T>().ToList();

        public virtual T Get(T entity) => _context.Set<T>().SingleOrDefault(e => e.Id == entity.Id);

        public virtual T Get(long? id) => _context.Set<T>().SingleOrDefault(e => e.Id == id);

        public virtual List<T> Get(Expression<Func<T, bool>> predicate, params string[] navProperties)
        {
            var query = this._context.Set<T>().Where(predicate);

            foreach (var navProperty in navProperties)
            {
                query = query.Include(navProperty);
            }

            return query.ToList();
        }

        public Task<T> SaveAsync(T entity)
        {
            try
            {
                _context.AddAsync(entity);
                _context.SaveChangesAsync();
            }
            catch (System.Exception ex)
            {
                throw new Exception("FAlha ao tentar salvar entidade assincrona", ex);
            }

            return Task.FromResult(entity);
        }

        public IEnumerable<T> SaveRange(IEnumerable<T> entityList)
        {
            try
            {
                _context.AddRange(entityList);
                _context.SaveChanges();
            }
            catch (System.Exception ex)
            {
                throw new Exception("Falha ao tentar salvar entidades", ex);
            }

            return entityList;
        }

        public Task<IEnumerable<T>> SaveRangeAsync(IEnumerable<T> entityList)
        {
            try
            {
                _context.AddRangeAsync(entityList);
                _context.SaveChangesAsync();
            }
            catch (System.Exception ex)
            {
                throw new Exception("Falha ao tentar salvar as entidades", ex);
            }

            return Task.FromResult(entityList);
        }

    }
}
