/*
 * vim:noexpandtab:sw=4:sts=0:ts=4:syn=cs
 */

namespace Abraca {
	public class MainHPaned : Gtk.HPaned {
		private CollectionsTree _coll_tree;
		private RightHPaned _right_hpaned;

		public CollectionsTree collections_tree {
			get {
				return _coll_tree;
			}
		}

		public RightHPaned right_hpaned {
			get {
				return _right_hpaned;
			}
		}

		construct {
			position = 120;
			position_set = false;

			create_widgets();
		}

		public void eval_config() {
			int pos = Abraca.instance().config.panes_pos1;

			position = pos.clamp(120, 800);

			/* other widgets */
			_right_hpaned.eval_config();
		}

		private void create_widgets() {
			Gtk.ScrolledWindow scrolled = new Gtk.ScrolledWindow(
				null, null
			);

			scrolled.set_policy(Gtk.PolicyType.NEVER,
			                    Gtk.PolicyType.AUTOMATIC);
			scrolled.set_shadow_type(Gtk.ShadowType.IN);

			_coll_tree = new CollectionsTree();
			scrolled.add(_coll_tree);

			pack1(scrolled, false, true);

			_right_hpaned = new RightHPaned();
			pack2(_right_hpaned, true, true);
		}
	}
}
